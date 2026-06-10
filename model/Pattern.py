from Neonaure.Cell import Cell


class Pattern():


    """
    classe motif : réuni plusieurs case dans un motif. Les nombres
    """

    def init(self,motif_id : int,case : list[Cell]):
        self._id : int = motif_id
        self.cells : list[Cell] = case

    @property
    def size(self) -> int:
        return len(self.cells)


    @property
    def expected_values(self) -> set:
        return set(range(1, self.size + 1))


    @property
    def current_values(self) -> set:
        return {cell.get_value() for cell in self.cells if not cell.is_empty}


    @property
    def filled_values(self) -> list:
        return [cell.get_value() for cell in self.cells if not cell.is_empty]


    def is_complete(self) -> bool:
        return self.current_values == self.expected_values


    def contains_value(self, val: int) -> bool:
        return val in self.current_values


    def has_duplicate(self) -> bool:
        filled = self.filled_values
        return len(filled) != len(set(filled))


    def missing_values(self) -> set:
        return self.expected_values - self.current_values


    def add_cell(self, cell) -> None:
        self.cells.append(cell)
        cell.set_modif_id(self._id)


    def get_cell_positions(self) -> list:
        return [(cell.get_row(), cell.get_column()) for cell in self.cells]
