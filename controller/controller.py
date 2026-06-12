import logging, random
from tools.json_handler import JSONLoader
from PyQt6.QtWidgets import QFileDialog
from model.Grid import Grid
from model.solveur import Solver
from model.Grid_Generator import generation

class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        
        self._historic = []

        #! Temporary (View need to implement another function)
        self._view.signal_reset_grid.connect(self.handle_reset)
        self._view.signal_undo.connect(self.handle_undo)
        self._view.signal_save_grid.connect(self.handle_save)
        self._view.signal_load_grid.connect(self.handle_load)
        self._view.signal_solve_grid.connect(self.handle_solve)
        self._view.signal_cell_changed.connect(self.update_cell_value)
        self._view.signal_background_change.connect(self.on_change_background)
        self._view.signal_hint.connect(self.give_hint)
        self._view.signal_generate_grid.connect(self.handle_generate)

        self._view.show()
        self._load_game()

    def handle_reset(self):
        self._model.reset_user_values()
        self.refresh_view()

    def handle_undo(self):
        if len(self._historic) != 0:
            self._model.restore_state(self._historic.pop())
            self.refresh_view()

    def handle_save(self,path):
        try:
            self._model.to_json(path)
        except Exception as e:
            logging.error(e)

    def handle_load(self,path):
        try : 
            self._model.from_json(path)
            self._historic.clear()
            self._view.rebuild_grid(self._model._row, self._model._column)
            self._init_view_from_model()
            
        except Exception as e:
            logging.error(e)

    def handle_solve(self):
        self._historic.append(self._model.get_state())
        solver = Solver(self._model)
        solver.solve()
        self._init_view_from_model()
    
    def handle_generate(self, row : int = 5, col: int = 5, pourcentage_given: float = 0.35):
        print(f"[DEBUG] handle_generate appelé : row={row}, col={col}, pct={pourcentage_given}")
        nb_pattern = (row * col) // 3
        print(f"[DEBUG] Lancement génération...")
        new_grid = generation(row, col, nb_pattern, pourcentage_given)
        print(f"[DEBUG] Résultat génération : {new_grid}")
        if new_grid is None:
            print("Generation failed : ... retry")
            return
        self._model = new_grid
        self._historic.clear()
        self._view.rebuild_grid(self._model._row, self._model._column)
        self._init_view_from_model()
          
    def give_hint(self) -> bool:
        self._historic.append(self._model.get_state())
        
        solver = Solver(self._model)
        solver.solve()
        
        state = self._model.get_state()
        hint_cells = []
        ancient_state = self._historic.pop()
        for (r, c), (val, given, pid) in state.items():
            if not given and val != 0 and ancient_state[(r,c)][0] == 0:
                hint_cells.append((r, c, val))
        
        self._model.restore_state(ancient_state)
        
        if hint_cells:
            r, c, val = random.choice(hint_cells)
            print(f"Hint: ({r},{c}) = {val}")
            self._historic.append(self._model.get_state())
            self._model.set_value((r, c), val)
            self._view.update_cell(r, c, val)
            self._check_cell_error(r, c)
            for neighbor in self._model.get_neighbors(r, c):
                self._check_cell_error(neighbor.get_row(), neighbor.get_column())
            pattern_id = self._model.get_cell((r, c)).get_pattern_id()
            pattern = self._model.get_pattern(pattern_id)
            for cell in pattern.get_cells():
                self._check_cell_error(cell.get_row(), cell.get_column())
            
            self._view.start_hint_cooldown(60)
            
            if self._model.is_solved():
                self._view.show_victory()
            return True
        return False
               
    def update_cell_value(self, row, col, text):
        self._historic.append(self._model.get_state())
        value = int(text) if text else 0
        self._model.set_value((row, col), value)
        
        self._check_cell_error(row, col)

        for neighbor in self._model.get_neighbors(row, col):
            nr, nc = neighbor.get_row(), neighbor.get_column()
            neighbor_ok = self._model.check_neighbor_constraint(nr, nc)
            pattern_id = self._model.get_cell((nr, nc)).get_pattern_id()
            pattern_ok = self._model.check_pattern_constraint(pattern_id)
            self._view.update_cell_error(nr, nc, not neighbor_ok or not pattern_ok)

        pattern_id = self._model.get_cell((row, col)).get_pattern_id()
        pattern = self._model.get_pattern(pattern_id)
        for cell in pattern.get_cells():
            self._check_cell_error(cell.get_row(), cell.get_column())

        if self._model.is_solved():
            self._view.show_victory()

    def _check_cell_error(self, row, col):
        neighbor_ok = self._model.check_neighbor_constraint(row, col)

        cell = self._model.get_cell((row, col))
        cell_val = cell.get_value()
        pattern_ok = True
        if cell_val != 0:
            pattern = self._model.get_pattern(cell.get_pattern_id())
            count = sum(1 for c in pattern.get_cells() if c.get_value() == cell_val)
            if count > 1:
                pattern_ok = False

        is_error = not neighbor_ok or not pattern_ok
        self._view.update_cell_error(row, col, is_error)
        
    def refresh_view(self):
        for r in range(self._model._row):
            for c in range(self._model._column):
                val = self._model.get_cell((r, c)).get_value()
                self._view.update_cell(r, c, val)


    def _init_view_from_model(self):
        for r in range(self._model._row):
            for c in range(self._model._column):
                cell = self._model.get_cell((r, c))
                val = cell.get_value()

                if cell.get_given():
                    # Show value and lock cell
                    self._view.set_cell_readonly(r, c, val)
                elif val != 0:
                    # Show user-filled value
                    self._view.update_cell(r, c, val)
                # borders
                borders = self._model.get_pattern_border(r, c)
                self._view.grid_widget.set_cell_borders(
                    r, c, 
                    borders["top"], borders["right"], 
                    borders["bottom"], borders["left"]
                )
    def on_change_background(self,path : str):
        self._view.set_background(path)
        
    def _load_game(self) : 
        self._model.from_json("examples/grille2.json")
        self._init_view_from_model()



