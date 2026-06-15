from model.Cell import Cell
from model.Pattern import Pattern
from tools.json_handler import JSONLoader
import json
import numpy as np
import numpy.typing as npt
from typing import List, Tuple, Set, Dict, Any, Union

class Grid:
    
    """
    
    Attribut : 
    
    cell : Matrice 2D des cellules
    patterns : Dictionnaire des patterns indexé par ID
    name : Nom de la grille 
    """

    _MOORE : List[Tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1),
                                        (0, -1),           (0, 1),
                                        (1, -1),  (1, 0),  (1, 1)] ## ? https://en.wikipedia.org/wiki/Moore_neighborhood
    """
    ! Visual représentation
    ! (-1, -1), (-1, 0), (-1, 1 )    ↖ ↑ ↗
    ! ( 0,-1)        ( 0,1)          ← · →
    ! (1,-1) ( 1,0) ( 1,1)           ↙ ↓ ↘
    """

    def __init__(self, shape: tuple, name: str) -> None:
        r, c = shape
        self.values      = np.zeros((r, c), dtype=int)
        self.given       = np.zeros((r, c), dtype=bool)
        self.pattern_ids = np.full((r, c), -1, dtype=int)
        self._name       = name

    @property
    def _row(self) -> int:    
        return self.values.shape[0]

    @property
    def _column(self)-> int:  
        return self.values.shape[1]

    def pattern_ids_set(self):
        return set(self.pattern_ids[self.pattern_ids >= 0].tolist())

    def pattern_cells(self, pid):
        """Return list of (row, col) for every cell in pattern *pid*."""
        return list(zip(*np.where(self.pattern_ids == pid)))

    def pattern_size(self, pid):
        return int(np.sum(self.pattern_ids == pid))

    def pattern_values(self, pid):
        """Non-zero values currently in pattern *pid*."""
        return set(self.values[self.pattern_ids == pid].tolist()) - {0}

    def pattern_has_duplicate(self, pid):
        vals = self.values[self.pattern_ids == pid]
        filled = vals[vals != 0]
        return len(filled) != len(set(filled)) if len(filled) else False

    def get_cell(self, coord):
        return Cell(self, coord[0], coord[1])

    def set_value(self, coord, val) -> None :
        self.values[coord[0], coord[1]] = val

    def get_neighbors(self, r, c):
        """Moore neighbourhood as list of (row, col)."""
        return [(r + dr, c + dc) for dr, dc in self._MOORE
                if 0 <= r + dr < self._row and 0 <= c + dc < self._column]

    def neighbor_values(self, r, c):
        return {self.values[nr, nc] for nr, nc in self.get_neighbors(r, c)}

    def check_neighbor_constraint(self, r, c):
        v = self.values[r, c]
        return v == 0 or v not in self.neighbor_values(r, c)

    def check_pattern_constraint(self, pid):
        return not self.pattern_has_duplicate(pid)

    def cell_has_pattern_duplicate(self, r, c):
        """True when this cell's value appears more than once in its pattern."""
        v = self.values[r, c]
        if v == 0:
            return False
        pid = self.pattern_ids[r, c]
        return int(np.sum((self.pattern_ids == pid) & (self.values == v))) > 1

    def _neighbor_conflicts(self):
        """True where a cell shares a value with a Moore neighbour."""
        conflict = np.zeros_like(self.values, dtype=bool)
        rows, cols = self.values.shape

        for dr, dc in self._MOORE:
            rs, re = max(0, -dr), min(rows, rows - dr)
            cs, ce = max(0, -dc), min(cols, cols - dc)
            same = (self.values[rs:re, cs:ce]
                    == self.values[rs + dr:re + dr, cs + dc:ce + dc])
            conflict[rs:re, cs:ce] |= same & (self.values[rs:re, cs:ce] != 0)
        return conflict


    def is_solved(self) -> bool :

        if np.any(self.values == 0):
            return False
        if np.any(self._neighbor_conflicts()):
            return False
        return not any(self.pattern_has_duplicate(p) for p in self.pattern_ids_set())

    def get_errors(self):
        errors = []

        for r, c in zip(*np.where(self._neighbor_conflicts())):
            errors.append((int(r), int(c), "neighbor"))
        for pid in self.pattern_ids_set():
            if self.pattern_has_duplicate(pid):
                for r, c in self.pattern_cells(pid):
                    errors.append((r, c, "pattern_duplicate"))
        return errors

    def reset_user_values(self) -> None:
        self.values[~self.given] = 0

    def get_state(self):
        return (self.values.copy(), self.given.copy(), self.pattern_ids.copy())

    def restore_state(self, state) -> bool:
        self.values, self.given, self.pattern_ids = (a.copy() for a in state)


    def get_pattern_border(self, r, c):
        pid = self.pattern_ids[r, c]
        def diff(dr, dc):
            nr, nc = r + dr, c + dc
            return (not (0 <= nr < self._row and 0 <= nc < self._column)
                    or self.pattern_ids[nr, nc] != pid)
        return {"top": diff(-1, 0), "bottom": diff(1, 0),
                "left": diff(0, -1), "right": diff(0, 1)}

    def from_json(self, path) -> None:
        grid_dict = JSONLoader.load_json(path)
        positions = [(t[1], t[0]) for ts in grid_dict.values() for t in ts]

        rows = max(r for r, _ in positions) + 1
        cols = max(c for _, c in positions) + 1

        self.values      = np.zeros((rows, cols), dtype=int)
        self.given       = np.zeros((rows, cols), dtype=bool)
        self.pattern_ids = np.full((rows, cols), -1, dtype=int)

        for key, triplets in grid_dict.items():
            pid = int(key[len("motif"):])
            for col, row, val in triplets:
                self.values[row, col]      = val
                self.given[row, col]       = val != 0
                self.pattern_ids[row, col] = pid

    def to_json(self, path) -> None:
        d = {}

        for pid in sorted(self.pattern_ids_set()):
            d[f"motif{pid}"] = [
                [c, r, int(self.values[r, c]) if self.given[r, c] else 0]
                for r, c in self.pattern_cells(pid)
            ]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)

        

