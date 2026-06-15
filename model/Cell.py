class Cell():

    """Classe représentant une case

    Attribut : 

    row : ligne de la case dans la grille
    column : colonne de la case dans la grille
    value : valeur de la case
    given : True si la valeur est une valeur donnée dès le départ sinon False
    motif_id : le numero du motif auquelle la case appartient

    Méthode : 

    is_empty : retourne True si la case n'a pas de valeur sinon False
    set_value : setter pour attribuer une valeur à la case
    get_row : retourne le numéro de la ligne de la case
    get_column : retourne le numéro de la colonne de la case 
    get_value : retourne la valeur de la case
    get_given : retourne True si une valeur était déja inscrite sinon False
    get pattern_id : retourne le numéro du motif auquelle la case appartient


    """
    def __init__(self, grid, row: int, col: int):
        self._grid = grid
        self._row = row
        self._col = col

    def is_empty(self) -> bool:
        return self._grid.values[self._row, self._col] == 0

    def get_row(self) -> int:
        return self._row

    def get_column(self) -> int:
        return self._col

    def get_value(self) -> int:
        return int(self._grid.values[self._row, self._col])

    def get_given(self) -> bool:
        return bool(self._grid.given[self._row, self._col])

    def get_pattern_id(self) -> int:
        return int(self._grid.pattern_ids[self._row, self._col])

    def set_value(self, val: int) -> None:
        self._grid.values[self._row, self._col] = val

    def set_pattern_id(self, pid: int) -> None:
        self._grid.pattern_ids[self._row, self._col] = pid

    def set_given(self, flag: bool) -> None:
        self._grid.given[self._row, self._col] = flag

    def __str__(self) -> str:
        return f"{self._row},{self._col},{self.get_given()},{self.get_pattern_id()},{self.get_value()}"
