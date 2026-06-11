from model.Cell import Cell
from model.Pattern import Pattern
from ..tools.json_handler import JSONLoader
import json

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
    
    def get_pattern_dict(self) -> dict:
        return self._patterns
    
    def get_pattern(self,pattern_id : int) -> Pattern:
        return self._patterns[pattern_id]
    
    def get_neighbors(self,row : int,col : int) -> list[Cell]:
        Cell_list : list[Cell] = []
        for x in range(row - 1, row + 2):
            for y in range(col - 1, col + 2):
                if x == row and y == col:
                    continue                          # skip cell itself; bug fix
                if x >= 0 and x < self._row:
                    if y >= 0 and y < self._column:
                        if x != row or y != col:
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
        for row in range(self._row):
            for col in range(self._column):
                if self.get_cell((row,col)).get_value() == 0:
                    return False
                if not self.check_neighbor_constraint(row,col):
                    return False
                
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
    
    def set_value(self,coord : tuple, valeur : int) ->None:
        self._cell[coord[0]][coord[1]].set_value(valeur)
        
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
                self._cell[row][col].set_pattern_id(state[(row,col)][2])
                
    def get_pattern_border(self, row: int, col: int) -> dict:
        pattern_border = {}
        currently_case = self._cell[row][col]
        current_id = currently_case.get_pattern_id()
     
        pattern_border["top"] = (row == 0) or (self._cell[row - 1][col].get_pattern_id() != current_id)
        
        pattern_border["bottom"] = (row == self._row - 1) or (self._cell[row + 1][col].get_pattern_id() != current_id)
        
        pattern_border["left"] = (col == 0) or (self._cell[row][col - 1].get_pattern_id() != current_id)
        
        pattern_border["right"] = (col == self._column - 1) or (self._cell[row][col + 1].get_pattern_id() != current_id)
            
        return pattern_border
    
    def from_json(self, path : str) -> None: 
        grid_dict : dict = JSONLoader.load_json(path)

        max_row : int = 0
        max_col : int = 0
        for triplets in grid_dict.values():
            for triplet in triplets:
                max_row = max(max_row,triplet[0])
                max_col = max(max_col,triplet[1])
        
        self._row = max_row + 1
        self._column = max_col + 1
        
        self._cell = [[None for truc in range(self._column)] for elt in range(self._row)]
        self._patterns = {}
        
        for pattern_key, triplets in grid_dict.items():
            pattern_id = int(pattern_key[len("motif"):])
            pattern = Pattern(pattern_id,[])
            self._patterns[pattern_id] = pattern
            
            for triplet in triplets:
                col, row, val = triplet[0], triplet[1], triplet[2]
                cell = Cell(row,col,val,pattern_id)
                self._cell[row][col] = cell
                pattern.add_cell(cell)
        
    def to_json(self, path : str) : 
        grid_dict : dict = {}
        
        for pattern_id,pattern in self._patterns.items():
            pattern_key = "motif" + str(pattern_id)
            triplets = []
            
            for cell in pattern.cells:
                val = cell.get_value() if cell.get_given() else 0
                triplets.append([cell.get_column(), cell.get_row(), val])
                
            grid_dict[pattern_key] = triplets
            
        """JSONLoader.save_json(path, grid_dict)"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(grid_dict, f, ensure_ascii=False, indent=2)
        

