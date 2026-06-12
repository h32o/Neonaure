from model.Grid import Grid
from model.Cell import Cell
import sys
import os


class Solver():
    def __init__(self, grid : Grid):
        self._grid : Grid = grid
    
    def get_domain(self, cell):
        pattern = self._grid.get_pattern(cell.get_pattern_id())
        value_list = list(range(1, pattern.size + 1))
        neighbor_values = {c.get_value() for c in self._grid.get_neighbors(cell.get_row(), cell.get_column())}
        # Correction : conversion explicite en set
        value_set = set(value_list) - set(pattern.current_values) - neighbor_values
        if not value_set:
            print(f"[DEBUG] domaine vide en ({cell.get_row()},{cell.get_column()}) pattern_size={pattern.size} current={pattern.current_values} neighbors={neighbor_values}")
        return list(value_set)
    
    def choose_cell(self) -> Cell:
        minimal_cell = None
        minimal_domain = float('inf')
        
        for pattern in self._grid.get_pattern_dict().values():
            for cell in pattern.get_cells():
                if cell.is_empty():
                    domain_size = len(self.get_domain(cell))
                    if domain_size < minimal_domain:
                        minimal_domain = domain_size
                        minimal_cell = cell
        
        return minimal_cell
            
    def solve(self) -> bool:
        if self._grid.is_solved():
            return True
        
        cell_to_fill = self.choose_cell()
        
        if cell_to_fill == None:
            return False
        
        domain = self.get_domain(cell_to_fill)
        if domain == [] : 
            return False
        
        for each_value in domain:
            cell_to_fill.set_value(each_value)
            
            if self.solve():
                return True
            cell_to_fill.set_value(0)
        
        return False

if __name__ == "__main__":
    
    
    # Ajouter le dossier parent pour que les imports fonctionnent
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Charger le JSON
    json_path = input("Chemin du fichier JSON : ")
    
    grid = Grid((0, 0), "test")
            
    grid.from_json(json_path)
    
    # Afficher la grille avant résolution
    print("\nGrille avant résolution :")
    for row in range(grid._row):
        for col in range(grid._column):
            val = grid.get_cell((row, col)).get_value()
            print(val if val != 0 else ".", end=" ")
        print()
    
    # Lancement du  solveur
    print("\nRésolution en cours...")
    solver = Solver(grid)
    result = solver.solve()
    
    # Affichage du résultat
    print(f"\nRésolu : {result}")
    
    if result:
        print("\nGrille après résolution :")
        for row in range(grid._row):
            for col in range(grid._column):
                print(grid.get_cell((row, col)).get_value(), end=" ")
            print()
    else:
        print("Aucune solution trouvée.")