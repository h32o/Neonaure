import logging, random
from tools.json_handler import JSONLoader
from view.main_window import MainWindow
from view.menu_window import MenuWindow

class Controller:
    def __init__(self, model, app_window):
        self._model = model
        self._app_window = app_window     

        self._menu_page = app_window.menu_page
        self._game_page = app_window.game_page

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
        self._game_page.signal_save_grid.connect(self.handle_save)
        self._game_page.signal_load_grid.connect(self.handle_load)
        self._game_page.signal_solve_grid.connect(self.handle_solve)
        self._game_page.signal_cell_changed.connect(self.update_cell_value)
        self._app_window.stack.setCurrentIndex(1)
        self._load_game()

    def handle_reset(self):
        self._model.reset_user_values()
        self.refresh_view()

    def handle_undo(self):
        pass
        """
        if self.model.undo():
            self.refresh_view()
        """

    def handle_save(self):
        try:
            print("TODO")
        except Exception as e:
            logging.error(e)

    def handle_load(self):

        try:
            self.refresh_view()
        except Exception as e:
            logging.error(e)

    def handle_solve(self):
        pass

    def update_cell_value(self, row, col, text):
        value = int(text) if text else 0
        self._model.set_value((row, col), value)

        neighbor_ok = self._model.check_neighbor_constraint(row, col)

        pattern_id = self._model.get_cell((row, col)).get_pattern_id()
        pattern_ok = self._model.check_pattern_constraint(pattern_id)

        is_error = not neighbor_ok or not pattern_ok
        self._game_page.update_cell_error(row, col, is_error)

    def refresh_view(self):
        for r in range(8):
            for c in range(8):
                val = self._model.get_cell((r,c)).get_value()
                self._game_page.update_cell(r, c, val)


    def _init_view_from_model(self):
        for r in range(self._model._row):
            for c in range(self._model._column):
                cell = self._model.get_cell((r, c))
                val = cell.get_value()

                if cell.get_given():
                    # Show value and lock cell
                    self._game_page.set_cell_readonly(r, c, val)

                # borders
                borders = self._model.get_pattern_border(r, c)
                self._game_page.grid_widget.set_cell_borders(
                    r, c, 
                    borders["top"], borders["right"], 
                    borders["bottom"], borders["left"]
                )

    def _load_game(self) : 
        self._model.from_json("grille2.json")
        self._init_view_from_model()



