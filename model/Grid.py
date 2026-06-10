from Neonaure.Cell import Cell
from Neonaure.Pattern import Pattern
from functools import JSONLoader

class Grid:
    
    """
    
    Attribut : 
    
    cell : Matrice 2D des cellules
    patterns : Dictionnaire des patterns indexé par ID
    name : Nom de la grille 
    """
    def __init__(self,taille : tuple,Grid_name : str):
        
        self._row : int = taille[0]
        self._column : int = taille[1]
        self._cell : list[list[Cell]] = []
        self._patterns : dict[int, Pattern] = {}    
        self._name  : str = Grid_name   
        
    def get_cell(self,coord : tuple) -> Cell:
        return self._cell[coord[0]][coord[1]]
    
    def get_pattern(self,pattern_id : int) -> Pattern:
        return self._patterns[pattern_id]
    
    def get_neighbors(self,row : int,col : int) -> list[Cell]:
        Cell_list : list[Cell] = []
        for x in range(row - 1,row + 2):
            for y in range(col - 1,col + 2):
                if x >= 0 and x < self._row:
                    if y >= 0 and y < self._column:
                        Cell_list.append(self._cell[x][y])
        return Cell_list
                    
    def check_neighbor_constraint(self,row : int,col :int) -> bool:
        currently_case : Cell = self._cell[row][col]
        if currently_case.get_value() == 0:
            return True
        
        valid_list : list[Cell] = self.get_neighbors(row,col)
        for case in valid_list:
            if case.get_value() == currently_case.get_value():
                return False
        return True
    
    def check_pattern_constraint(self,pattern_id : int) -> bool:
        return False if self._patterns[pattern_id].has_duplicate() else True
    
    def is_solved(self) -> bool:
        for i in self._patterns.keys():
            if self._patterns[i].has_duplicate():
                return False
        return True
    
    def get_errors(self) ->  list[tuple]:
        error_list : list = []
        for row in range(self._row):
            for col in range(self._column):
                if not self.check_neighbor_constraint(row,col):
                    error_list.append((row,col,"neighbor"))
        for pattern_id in self._patterns:
            if self._patterns[pattern_id].has_duplicate():
                for cell in self._patterns[pattern_id].get_cell_positions():
                    error_list.append((cell[0],cell[1],"pattern_duplicate"))
        
        return error_list
    
    def reset_user_values(self) -> None:
        for row in range(self._row):
            for col in range(self._column):
                if not self._cell[row][col].get_given():
                    self._cell[row][col].set_value(0)
    
    def get_state(self) -> dict:
        saved_dico : dict = {}
        for row in range(self._row):
            for col in range(self._column):
                cell : Cell = self._cell[row][col]
                saved_dico[(row,col)] = (cell.get_value(),cell.get_given(),cell.get_pattern_id())
        return saved_dico
     
    def restore_state(self,state : dict) -> None:
        for row in range(self._row):
            for col in range(self._column):
                self._cell[row][col].set_value(state[(row,col)][0])
                self._cell[row][col].set_given(state[(row,col)][1])
                self._cell[row][col].set_pattern_if(state[(row,col)][2])
                
    def get_pattern_border(self, row: int, col: int) -> dict:
        pattern_border = {}
        currently_case = self._cell[row][col]
        current_id = currently_case.get_pattern_id()
     
        pattern_border["top"] = (row == 0) or (self._cell[row - 1][col].get_pattern_id() != current_id)
        
        pattern_border["bottom"] = (row == self._row - 1) or (self._cell[row + 1][col].get_pattern_id() != current_id)
        
        pattern_border["left"] = (col == 0) or (self._cell[row][col - 1].get_pattern_id() != current_id)
        
        pattern_border["right"] = (col == self._column - 1) or (self._cell[row][col + 1].get_pattern_id() != current_id)
            
        return pattern_border
    
    def from_json(self, path : str) : 
        return JSONLoader.load_json(path)

    def to_json(self, path : str) : 
        pass
        

