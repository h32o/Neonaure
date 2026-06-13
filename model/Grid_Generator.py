from model.Grid import Grid
from model.Cell import Cell
from model.Pattern import Pattern
import random


def generation(row, col, nb_pattern, pourcentage_given):
    
    moore_dirs = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    ortho_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for attempt in range(500):

        MAX_VAL = 4
        grid_vals = [[0] * col for _ in range(row)]

        def fill_grid(pos):
            if pos == row * col:
                return True
            r, c = divmod(pos, col)
            used = set()
            for dr, dc in moore_dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < row and 0 <= nc < col:
                    used.add(grid_vals[nr][nc])
            available = [v for v in range(1, MAX_VAL + 1) if v not in used]
            random.shuffle(available)
            for v in available:
                grid_vals[r][c] = v
                if fill_grid(pos + 1):
                    return True
                grid_vals[r][c] = 0
            return False

        if not fill_grid(0):
            continue 

        assigned  = [[-1] * col for _ in range(row)]
        pat_groups = {}   # pid -> list[(r, c)]
        pid = 1

        cells_list = [(r, c) for r in range(row) for c in range(col)]
        random.shuffle(cells_list)

        for sr, sc in cells_list:
            if assigned[sr][sc] != -1:
                continue

            target = random.choice([2, 2, 3])
            group      = [(sr, sc)]
            group_vals = {grid_vals[sr][sc]}
            assigned[sr][sc] = pid
            frontier   = [(sr, sc)]

            while len(group) < target and frontier:
                r2, c2 = random.choice(frontier)
                candidates = []
                for dr, dc in ortho_dirs:
                    nr, nc = r2 + dr, c2 + dc
                    if (0 <= nr < row and 0 <= nc < col
                            and assigned[nr][nc] == -1
                            and grid_vals[nr][nc] not in group_vals):
                        candidates.append((nr, nc))
                if candidates:
                    nr, nc = random.choice(candidates)
                    assigned[nr][nc] = pid
                    group.append((nr, nc))
                    group_vals.add(grid_vals[nr][nc])
                    frontier.append((nr, nc))
                else:
                    frontier.remove((r2, c2))
            if len(group) == 1:
                sr0, sc0 = group[0]
                v0 = grid_vals[sr0][sc0]
                dirs_copy = list(ortho_dirs)
                random.shuffle(dirs_copy)
                merged = False
                for dr, dc in dirs_copy:
                    nr, nc = sr0 + dr, sc0 + dc
                    if 0 <= nr < row and 0 <= nc < col and assigned[nr][nc] != -1:
                        npid   = assigned[nr][nc]
                        ngroup = pat_groups[npid]
                        nvals  = {grid_vals[r][c] for r, c in ngroup}
                        if len(ngroup) < 3 and v0 not in nvals:
                            ngroup.append((sr0, sc0))
                            assigned[sr0][sc0] = npid
                            merged = True
                            break
                if merged:
                    continue

            pat_groups[pid] = group
            pid += 1

        # Vérifications d'intégrité
        if any(assigned[r][c] == -1 for r in range(row) for c in range(col)):
            continue
        if any(len(g) == 1 for g in pat_groups.values()):
            continue
        valid_pats = all(
            len({grid_vals[r][c] for r, c in g}) == len(g)
            for g in pat_groups.values()
        )
        if not valid_pats:
            for p_id, group in pat_groups.items():
                valeurs_actuelles = sorted(set(grid_vals[r][c] for r, c in group))
                correspondance = {ancien: nouveau for nouveau, ancien in enumerate(valeurs_actuelles, start=1)}
                for r, c in group:
                    grid_vals[r][c] = correspondance[grid_vals[r][c]]

            moore_ok = True
            for r in range(row):
                for c in range(col):
                    for dr, dc in moore_dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < row and 0 <= nc < col:
                            if grid_vals[r][c] == grid_vals[nr][nc]:
                                moore_ok = False
                                break
                    if not moore_ok:
                        break
                if not moore_ok:
                    break

            if not moore_ok:
                continue
        final_grid = Grid((row, col), "gen")
        final_grid._cell     = [[None] * col for _ in range(row)]
        final_grid._patterns = {}

        for p_id, group in pat_groups.items():
            pat = Pattern(p_id, [])
            final_grid._patterns[p_id] = pat
            for r, c in group:
                cell = Cell(r, c, grid_vals[r][c], p_id)
                final_grid._cell[r][c] = cell
                pat.cells.append(cell)

        toutes = [final_grid._cell[r][c] for r in range(row) for c in range(col)]
        random.shuffle(toutes)
        nb_garder = max(1, int(len(toutes) * pourcentage_given))
        for i, cell in enumerate(toutes):
            if i < nb_garder:
                cell.set_given(True)
            else:
                cell.set_given(False)
                cell.set_value(0)

        return final_grid
    return None