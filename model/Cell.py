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
    def __init__(self,row : int,column :int,val : int,motif_id : int):

        self._row : int = row
        self._column : int = column
        self._value : int = val
        self._given : bool = True if val != 0 else False
        self._motif_id : int = motif_id


    def is_empty(self) -> bool:
        return False if self._value != 0 else True

    
    def get_row(self) -> int:
        return self._row

    def get_column(self) -> int:
        return self._column

    def get_value(self) -> int:
        return self._value

    def get_given(self) -> bool:
        return self._given

    def get_pattern_id(self) -> int:
        return self._motif_id

    def set_value(self,values : int) -> None:
        self._value = values

    def set_pattern_id(self,id : int) -> None:
        self._motif_id = id

    def set_given(self,boolean : bool) -> None:
        self._given = boolean

    def __str__(self) -> str:
        return f"{self.get_row()},{self.get_column()},{self.get_given()},{self.get_pattern_id()},{self.get_value()}"