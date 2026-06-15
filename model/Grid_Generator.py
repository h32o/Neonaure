from model.Grid import Grid
from model.Cell import Cell
from model.Pattern import Pattern
import random


def generation(row, col, nb_pattern, pourcentage_given):
    
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

    for _ in range(500):
        MAX_VAL = 4
        grid_vals = [[0] * col for _ in range(row)]

        def fill(pos):
            if pos == row * col:
                return True

            r, c = divmod(pos, col)
            used = {grid_vals[r + dr][c + dc]
                    for dr, dc in moore_dirs
                    if 0 <= r + dr < row and 0 <= c + dc < col}
            avail = [v for v in range(1, MAX_VAL + 1) if v not in used]
            random.shuffle(avail)

            for v in avail:
                grid_vals[r][c] = v
                if fill(pos + 1):
                    return True
                grid_vals[r][c] = 0
            return False

        if not fill(0):
            continue


        assigned = [[-1] * col for _ in range(row)]
        pat_groups = {}
        pid = 1

        cells_list = [(r, c) for r in range(row) for c in range(col)]
        random.shuffle(cells_list)

        for sr, sc in cells_list:

            if assigned[sr][sc] != -1:
                continue
            target = random.choice([2, 2, 3])
            group = [(sr, sc)]
            group_vals = {grid_vals[sr][sc]}
            assigned[sr][sc] = pid
            frontier = [(sr, sc)]

            while len(group) < target and frontier:

                r2, c2 = random.choice(frontier)
                cands = [(r2 + dr, c2 + dc) for dr, dc in ortho_dirs
                         if 0 <= r2 + dr < row and 0 <= c2 + dc < col
                         and assigned[r2 + dr][c2 + dc] == -1
                         and grid_vals[r2 + dr][c2 + dc] not in group_vals]

                if cands:
                    nr, nc = random.choice(cands)
                    assigned[nr][nc] = pid
                    group.append((nr, nc))
                    group_vals.add(grid_vals[nr][nc])
                    frontier.append((nr, nc))
                else:
                    frontier.remove((r2, c2))

      
            if len(group) == 1:
                sr0, sc0 = group[0]
                v0 = grid_vals[sr0][sc0]
                merged = False
                dirs = list(ortho_dirs)
                random.shuffle(dirs)
                
                for dr, dc in dirs:
                    nr, nc = sr0 + dr, sc0 + dc
                    if 0 <= nr < row and 0 <= nc < col and assigned[nr][nc] != -1:
                        npid = assigned[nr][nc]
                        ng = pat_groups[npid]
                        nv = {grid_vals[r][c] for r, c in ng}
                        if len(ng) < 3 and v0 not in nv:
                            ng.append((sr0, sc0))
                            assigned[sr0][sc0] = npid
                            merged = True
                            break
                if merged:
                    continue

            pat_groups[pid] = group
            pid += 1


        if any(assigned[r][c] == -1 for r in range(row) for c in range(col)):
            continue
        if any(len(g) == 1 for g in pat_groups.values()):
            continue

        valid = all(len({grid_vals[r][c] for r, c in g}) == len(g)
                     for g in pat_groups.values())
        if not valid:
            for p_id, group in pat_groups.items():
                cur = sorted({grid_vals[r][c] for r, c in group})
                mapping = {old: new for new, old in enumerate(cur, 1)}
                for r, c in group:
                    grid_vals[r][c] = mapping[grid_vals[r][c]]
   
            ok = all(
                grid_vals[r][c] != grid_vals[r + dr][c + dc]
                for r in range(row) for c in range(col)
                for dr, dc in moore_dirs
                if 0 <= r + dr < row and 0 <= c + dc < col
            )
            if not ok:
                continue

        grid = Grid((row, col), "gen")
        grid.values      = np.array(grid_vals, dtype=int)
        grid.pattern_ids = np.array(assigned, dtype=int)
        grid.given       = np.zeros((row, col), dtype=bool)

        all_cells = [(r, c) for r in range(row) for c in range(col)]
        random.shuffle(all_cells)
        nb_keep = max(1, int(len(all_cells) * pourcentage_given))
        for i, (r, c) in enumerate(all_cells):
            if i < nb_keep:
                grid.given[r, c] = True
            else:
                grid.values[r, c] = 0
