from model.Grid import Grid
from model.Cell import Cell
from model.Pattern import Pattern
import numpy as np
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
import os


def _try_generation(args):
    row, col, pourcentage_given, max_solver_steps, _seed = args

    # Re-seed so each worker explores a different part of the search space
    if _seed is not None:
        random.seed(_seed) #? Change seed each time, one of the thing actually hinted by Mr Conoir as far as I understood, I'd really cry if he has a generator that is only 50 lines ;-;
    
    moore_dirs = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    """
    ! Visual représentation
    ! (-1, -1), (-1, 0), (-1, 1 )    ↖ ↑ ↗
    ! ( 0,-1)        ( 0,1)          ← · →
    ! (1,-1) ( 1,0) ( 1,1)           ↙ ↓ ↘
    """

    ortho_dirs = [(-1, 0), #! ↑
                 (1, 0),   #! ↓
                 (0, -1),  #! ←
                 (0, 1)]   #! →

    #  Generate pattern layout (regions of size 4-5)
    assigned = [[-1] * col for _ in range(row)]
    pat_groups = {}
    pid = 1

    cells_list = [(r, c) for r in range(row) for c in range(col)]
    random.shuffle(cells_list)

    for sr, sc in cells_list:
        if assigned[sr][sc] != -1:
            continue
        target = random.choice([4, 5, 5])
        group = [(sr, sc)]
        assigned[sr][sc] = pid
        frontier = [(sr, sc)]

        while len(group) < target and frontier:
            r2, c2 = random.choice(frontier)
            cands = [(r2 + dr, c2 + dc) for dr, dc in ortho_dirs
                     if 0 <= r2 + dr < row and 0 <= c2 + dc < col
                     and assigned[r2 + dr][c2 + dc] == -1]
            if cands:
                nr, nc = random.choice(cands)
                assigned[nr][nc] = pid
                group.append((nr, nc))
                frontier.append((nr, nc))
            else:
                frontier.remove((r2, c2))

        # Handle size-1 groups: merge with a neighbor's group
        if len(group) == 1:
            sr0, sc0 = group[0]
            merged = False
            dirs = list(ortho_dirs)
            random.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = sr0 + dr, sc0 + dc
                if 0 <= nr < row and 0 <= nc < col and assigned[nr][nc] != -1:
                    npid = assigned[nr][nc]
                    ng = pat_groups[npid]
                    if len(ng) < 5:
                        ng.append((sr0, sc0))
                        assigned[sr0][sc0] = npid
                        merged = True
                        break
            if merged:
                continue

        pat_groups[pid] = group
        pid += 1


    if any(assigned[r][c] == -1 for r in range(row) for c in range(col)):
        return None
    if any(len(g) == 1 for g in pat_groups.values()):
        return None

    grid = Grid((row, col), "gen")
    grid.pattern_ids = np.array(assigned, dtype=int)
    grid.values      = np.zeros((row, col), dtype=int)
    grid.given       = np.zeros((row, col), dtype=bool)

    pid_arr = grid.pattern_ids

    max_pid = int(pid_arr.max()) + 1
    pat_cells = {}   #! pid -> list of (r, c)
    pat_sizes = {}   #! pid -> int
    for p in range(max_pid):
        cells = list(zip(*np.where(pid_arr == p)))
        if cells:
            pat_cells[p] = cells
            pat_sizes[p] = len(cells)

    #  Pre-compute Moore neighbour lists for every cell
    neighbor_map = {}
    for r in range(row):
        for c in range(col):
            neighbor_map[(r, c)] = [
                (r + dr, c + dc) for dr, dc in moore_dirs
                if 0 <= r + dr < row and 0 <= c + dc < col
            ]

    #  Mutable solver state (avoids re-scanning the grid every call)
    pat_used = {p: set() for p in pat_cells}   #! values used per pattern
    cell_val = grid.values                       #! alias for speed
    unfilled = row * col                         #! replaces grid.is_solved() scan
    steps = 0

    def _get_domain(r, c):
        #! O(1) set lookups instead of grid.pattern_values() + grid.neighbor_values()
        p = pid_arr[r, c]
        used = set(pat_used[p])
        for nr, nc in neighbor_map[(r, c)]:
            v = cell_val[nr, nc]
            if v != 0:
                used.add(v)
        return [v for v in range(1, pat_sizes[p] + 1) if v not in used]

    def _choose_cell():
        #! MRV heuristic: pick the unfilled cell with the smallest domain
        best, best_len = None, 10
        for r in range(row):
            for c in range(col):
                if cell_val[r, c] == 0:
                    d = len(_get_domain(r, c))
                    if d < best_len:
                        best, best_len = (r, c), d
                        if d == 0:
                            return best  # fail fast
        return best

    def _solve():
        nonlocal unfilled, steps
        steps += 1
        if steps > max_solver_steps:
            return False

        #! All cells filled? (replaces grid.is_solved() full scan)
        if unfilled == 0:
            if not np.any(grid._neighbor_conflicts()):
                return True
            return False

        cell = _choose_cell()
        if cell is None:
            return False
        r, c = cell
        p = pid_arr[r, c]
        avail = _get_domain(r, c)
        random.shuffle(avail)
        for v in avail:
            cell_val[r, c] = v
            pat_used[p].add(v)
            unfilled -= 1

            #! Forward checking: if any neighbour or same-pattern cell
            #! now has an empty domain, backtrack immediately instead of
            #! exploring deeper into a dead branch
            dead_end = False
            for nr, nc in neighbor_map[(r, c)]:
                if cell_val[nr, nc] == 0 and not _get_domain(nr, nc):
                    dead_end = True
                    break
            if not dead_end:
                for pr, pc in pat_cells[p]:
                    if cell_val[pr, pc] == 0 and not _get_domain(pr, pc):
                        dead_end = True
                        break

            if not dead_end and _solve():
                return True

            # Undo
            cell_val[r, c] = 0
            pat_used[p].discard(v)
            unfilled += 1

        return False

    if not _solve():
        return None

   
    all_cells = [(r, c) for r in range(row) for c in range(col)]
    random.shuffle(all_cells)
    nb_keep = max(1, int(len(all_cells) * pourcentage_given))
    for i, (r, c) in enumerate(all_cells):
        if i < nb_keep:
            grid.given[r, c] = True
        else:
            grid.values[r, c] = 0

    return grid


def generation(row, col, nb_pattern, pourcentage_given,
               max_attempts=500, workers=None):

    max_solver_steps = row * col * 2000

    if workers is None:
        workers = min(os.cpu_count() or 4, 8)

    #  Each attempt gets a unique seed so workers explore different paths
    base_seed = random.randint(0, 2**31)
    args_list = [
        (row, col, pourcentage_given, max_solver_steps, base_seed + i)
        for i in range(max_attempts)
    ]

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_try_generation, args): idx
            for idx, args in enumerate(args_list)
        }

        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception:
                continue
            if result is not None:
                # Cancel everything that hasn't started yet
                for f in futures:
                    f.cancel()
                return result

    return None