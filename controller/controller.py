import logging 

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        #! Temporary (View need to implement another function)
        self.view.signal_reset_grid.connect(self.handle_reset)
        self.view.signal_undo.connect(self.handle_undo)
        self.view.signal_save_grid.connect(self.handle_save)
        self.view.signal_load_grid.connect(self.handle_load)
        self.view.signal_solve_grid.connect(self.handle_solve)

    def handle_reset(self):
        self.model.reset()
        self.refresh_view()

    def handle_undo(self):
        if self.model.undo():
            self.refresh_view()

    def handle_save(self):
        try:
            self.model.save_to_file("savegame.json")
        except Exception as e:
            logging.error(e)

    def handle_load(self):
        try:
            self.model.load_from_file("savegame.json")
            self.refresh_view()
        except Exception as e:
            logging.error(e)

    def handle_solve(self):
        pass

    def update_cell_value(self, row, col, value):
        success = self.model.update_cell(row, col, value)
        if success:
            is_valid, error = self.model.check_rules(row, col)
            if not is_valid:
                self.view.change_color_cell_error(row, col, True)
            else:
                self.view.change_color_cell_error(row, col, False)
            self.refresh_view()

    def refresh_view(self):
        for r in range(8):
            for c in range(8):
                val = self.model.grid[r][c]
                cell = self.view.cells[(r, c)]
                cell.setText(val)
