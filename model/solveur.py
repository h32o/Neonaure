from model.Grid import Grid
from model.Cell import Cell
import sys
import os


class Solver():
    def __init__(self, grid: Grid):
        self.g = grid

    def get_domain(self, r, c):
        pid = self.g.pattern_ids[r, c]
        used = self.g.pattern_values(pid) | self.g.neighbor_values(r, c)
        return [v for v in range(1, self.g.pattern_size(pid) + 1) if v not in used]

    def choose_cell(self):
        best, best_len = None, 10
        for r in range(self.g._row):
            for c in range(self.g._column):
                if self.g.values[r, c] == 0:
                    d = len(self.get_domain(r, c))
                    if d < best_len:
                        best, best_len = (r, c), d
                        if d == 0:
                            return best
        return best

    def solve(self) -> bool:
        if self.g.is_solved():
            return True
        cell = self.choose_cell()
        if cell is None:
            return False
        r, c = cell
        pid = self.g.pattern_ids[r, c]
        for v in self.get_domain(r, c):
            self.g.values[r, c] = v
            dead_end = False
            for nr, nc in self.g.get_neighbors(r, c):
                if self.g.values[nr, nc] == 0 and not self.get_domain(nr, nc):
                    dead_end = True
                    break
            if not dead_end:
                for pr, pc in self.g.pattern_cells(pid):
                    if self.g.values[pr, pc] == 0 and not self.get_domain(pr, pc):
                        dead_end = True
                        break
            if not dead_end and self.solve():
                return True
            self.g.values[r, c] = 0
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