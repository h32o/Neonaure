from Grid import Grid

class Solveur():
    def __init__(self, grid : Grid):
        self._grid : Grid = grid
    
    def minimize_domain(self) -> int:
        minimal_size : int = 10
        pattern_start : int = 0
        for nom in self._grid.get_pattern_dict().keys():
            if self._grid.get_pattern(nom).size() < minimal_size:
                pattern_start = nom
                minimal_size = self._grid.get_pattern(nom).size()
                
        return pattern_start
            
    def solve(self) -> Grid:
        if self._grid.is_solved():
            return self._grid
        
        