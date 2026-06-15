import logging, random
from tools.json_handler import JSONLoader
from view.main_window import MainWindow
from view.menu_window import MenuWindow
from model.solveur import Solver
from PySide6.QtWidgets import QApplication
from model.Grid_Generator import generation
from PySide6.QtCore import QThread, Signal as  pyqtSignal

class _GenerationWorker(QThread):
    grid_ready = pyqtSignal(object)

    def __init__(self, row, col, pourcentage_given, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.pourcentage_given = pourcentage_given

    def run(self):
        nb_pattern = (self.row * self.col) // 3
        try:
            result = generation(self.row, self.col, nb_pattern,
                                self.pourcentage_given)
        except Exception as exc:
            logging.error(f"Generation error: {exc}")
            result = None
        self.grid_ready.emit(result)

class Controller:
    def __init__(self, model, app_window):
        self._model = model
        self._app_window = app_window     

        self._menu_page = app_window.menu_page
        self._game_page = app_window.game_page

        self._historic = []
        self._historic_redo = []
        self._gen_worker = None
        
        self._app_window.showFullScreen()


        # Start on menu
        self._app_window.stack.setCurrentIndex(0)
        self._handle_main_menu()
        
    def _handle_main_menu(self):
        self._menu_page.signal_start_game.connect(self._handle_game_window)

    def _handle_game_window(self) : 
        
        #! Temporary (View need to implement another function)
        self._game_page.signal_reset_grid.connect(self.handle_reset)
        self._game_page.signal_undo.connect(self.handle_undo)
        self._game_page.signal_redo.connect(self.handle_redo)
        self._game_page.signal_save_grid.connect(self.handle_save)
        self._game_page.signal_load_grid.connect(self.handle_load)
        self._game_page.signal_solve_grid.connect(self.handle_solve)
        self._game_page.signal_cell_changed.connect(self.update_cell_value)
        self._game_page.signal_hint.connect(self.give_hint)
        self._game_page.signal_generate_grid.connect(self.handle_generate)
        self._app_window.stack.setCurrentIndex(1)
        self._load_game()

    def handle_reset(self):
        self._model.reset_user_values()
        self.refresh_view()

    def handle_undo(self):
        if len(self._historic) != 0:
            current = self._model.get_state()
            self._historic_redo.append(current)
            state = self._historic.pop()  
            self._model.restore_state(state)
            self.refresh_view()
            
    def handle_redo(self):
        if len(self._historic_redo) != 0:
            current = self._model.get_state()
            self._historic.append(current)
            state = self._historic_redo.pop()
            self._model.restore_state(state)
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
            self._game_page.rebuild_grid(self._model._row, self._model._column)
            self._init_view_from_model()
            
        except Exception as e:
            logging.error(e)

    def handle_solve(self):
        self._historic.append(self._model.get_state())
        Solver(self._model).solve()
        if self._model.is_solved():
            pass
        self._init_view_from_model()
    
    def handle_generate(self, row : int = 5, col: int = 5, pourcentage_given: float = 0.35):
        # If a generation is already running, ignore the request
        if self._gen_worker is not None and self._gen_worker.isRunning():
            return

        # Show loading overlay
        self._game_page.show_loading("Generating grid\u2026")

        # Launch worker thread
        self._gen_worker = _GenerationWorker(
            row, col, pourcentage_given, parent=self._app_window
        )
        self._gen_worker.grid_ready.connect(self._on_generation_done)
        self._gen_worker.start()

    def _on_generation_done(self, new_grid):
        """Called on the main thread when the worker finishes."""
        self._game_page.hide_loading()

        if new_grid is None:
            logging.warning("Generation failed: all attempts exhausted")
            return

        self._model = new_grid
        self._historic.clear()
        self._game_page.rebuild_grid(self._model._row, self._model._column)
        self._init_view_from_model()

    def give_hint(self) -> bool:
        old_values = self._model.values.copy()
        self._historic.append(self._model.get_state())
    
        solver = Solver(self._model)
        solver.solve()
    
        hint_cells = []
        for r in range(self._model._row):
            for c in range(self._model._column):
                if not self._model.given[r, c] and self._model.values[r, c] != 0 and old_values[r, c] == 0:
                    hint_cells.append((r, c, int(self._model.values[r, c])))
    
        self._model.restore_state(self._historic.pop())
    
        if hint_cells:
            r, c, val = random.choice(hint_cells)
            self._historic.append(self._model.get_state())
            self._model.set_value((r, c), val)
            self._game_page.update_cell(r, c, val)
            self._check_cell_error(r, c)
            for nr, nc in self._model.get_neighbors(r, c):
                self._check_cell_error(nr, nc)
            pid = self._model.pattern_ids[r, c]
            for cr, cc in self._model.pattern_cells(pid):
                self._check_cell_error(cr, cc)
    
            self._game_page.start_hint_cooldown(60)
    
            if self._model.is_solved():
                self._game_page.show_victory()
            return True
        return False

    def update_cell_value(self, row, col, text):
        self._historic.append(self._model.get_state())
        value = int(text) if text else 0
        self._model.set_value((row, col), value)

        self._check_cell_error(row, col)

        for nr, nc in self._model.get_neighbors(row, col):
            n_ok = self._model.check_neighbor_constraint(nr, nc)
            p_ok = self._model.check_pattern_constraint(self._model.pattern_ids[nr, nc])
            self._game_page.update_cell_error(nr, nc, not n_ok or not p_ok)

        for cr, cc in self._model.pattern_cells(self._model.pattern_ids[row, col]):
            self._check_cell_error(cr, cc)

        if self._model.is_solved():
            self._game_page.show_victory()

    def _check_cell_error(self, row, col):
        neighbor_ok = self._model.check_neighbor_constraint(row, col)
        pattern_ok  = not self._model.cell_has_pattern_duplicate(row, col)
        self._game_page.update_cell_error(row, col, not neighbor_ok or not pattern_ok)
        
    def refresh_view(self):
        for r in range(self._model._row):
            for c in range(self._model._column):
                val = self._model.get_cell((r, c)).get_value()
                self._game_page.update_cell(r, c, val)


    def _init_view_from_model(self):
        for r in range(self._model._row):
            for c in range(self._model._column):
                cell = self._model.get_cell((r, c))
                val = cell.get_value()

                if cell.get_given():
                    self._game_page.set_cell_readonly(r, c, val)
                elif val != 0:
                    self._game_page.update_cell(r, c, val)
                borders = self._model.get_pattern_border(r, c)
                self._game_page.grid_widget.set_cell_borders(r, c, 
                    borders["top"], borders["right"], 
                    borders["bottom"], borders["left"])
        
    def _load_game(self) : 
        self._model.from_json("grille2.json")
        self._init_view_from_model()
    
    def start_quit(self):
        
        QApplication.instance().quit()

