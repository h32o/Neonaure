from Neonaure.Case import Case
from Neonaure.Motif import Motif

class Grille:
    
    """
    
    Attribut : 
    
    cell : Matrice 2D des cellules
    motifs : Dictionnaire des motifs indexé par ID
    name : Nom de la grille 
    """
    def __init__(self,taille : tuple,Grid_name : str):
        
        self._row : int = taille[0]
        self._column : int = taille[1]
        self._cell : list[list[Case]] = []
        self._motifs : dict[int, Motif] = {}	
        self._name	: str = Grid_name	
        
    def get_cell(self,coord : tuple) -> Case:
        return self._cell[coord[0]][coord[1]]
    
    def get_motif(self,motif_id : int) -> Motif:
        return self._motifs[motif_id]
    
    def get_neighbors(self,row : int,col : int) -> list[Case]:
        Case_list : list[Case] = []
        for x in range(row - 1,row + 2):
            for y in range(col - 1,col + 2):
                if x >= 0 and x < self._row:
                    if y >= 0 and y < self._column:
                        Case_list.append(self._cell[x][y])
        return Case_list
                    
    def check_neighbor_constraint(self,row : int,col : int) -> bool:
        currently_case : Case = self._cell[row][col]
        if currently_case.get_value() == 0:
            return True
        
        valid_list : list[Case] = self.get_neighbors(row,col)
        for case in valid_list:
            if case.get_value() == currently_case.get_value():
                return False
        return True
    
    def check_motif_constraint(self,motif_id : int) -> bool:
        return False if self._motifs[motif_id].has_duplicate() else True
    
    def is_solved(self) -> bool:
        for i in range(self._motifs.keys()):
            if self._motifs[i].has_duplicate():
                return False
        return True
    
    def get_errors(self) ->  list[tuple]:
        error_list : list = []
        for row in range(self._row):
            for col in range(self._column):
                if not self.check_neighbor_constraint(row,col):
                    error_list.append((row,col,"neighbor"))
        for id in self._motifs:
            if self._motifs[id].has_duplicate():
                for cell in self._motifs[id].get_cell_positions():
                    error_list.append((cell[0],cell[1],"motif_duplicate"))
        
        return error_list
    
    def reset_user_values(self) -> None:
        for row in range(self._row):
            for col in range(self._col):
                if not self._cell[row][col].get_given():
                    self._cell[row][col].set_value(0)
    
    def get_state(self) -> dict:
        saved_dico : dict = {}
        for row in range(self._row):
            for col in range(self._col):
                cell : Case = self._cell[row][col]
                saved_dico[(row,col)] = (cell.get_value(),cell.get_given(),cell.get_motif_id())
        return saved_dico
     
    def restore_state(self,state : dict) -> None:
        for row in range(self._row):
            for col in range(self._col):
                self._cell[row][col].set_value(state[(row,col)][0])
                self._cell[row][col].set_given(state[(row,col)][1])
                self._cell[row][col].set_motif_if(state[(row,col)][2])
                
    def get_motif_border(self,row : int,col: int) ->dict:
        motif_border : dict = {}
        currently_case : Case = self._cell[row][col]
        if row == 0:
            motif_border["top"] = False
        elif self._cell[row - 1][col].get_motif_id() == currently_case.get_motif_id():
            motif_border["top"] = True
        else:
            motif_border["top"] = False
        
        if col == 0:
            motif_border["left"] = False
        elif self._cell[row ][col - 1].get_motif_id() == currently_case.get_motif_id():
            motif_border["left"] = True
        else:
            motif_border["left"] = False
        
        if row == self._row:
            motif_border["bottom"] = False
        elif self._cell[row + 1][col].get_motif_id() == currently_case.get_motif_id():
            motif_border["bottom"] = True
        else:
            motif_border["bottom"] = False
            
        if col == 0:
            motif_border["right"] = False
        elif self._cell[row ][col + 1].get_motif_id() == currently_case.get_motif_id():
            motif_border["right"] = True
        else:
            motif_border["right"] = False
            
        return motif_border
    
    """def from_json(self,data):"""
