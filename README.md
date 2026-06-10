# SAÉ Graphes-IHM — Néonaure

## Présentation

Le **Néonaure** est inspiré du Sudoku joué généralement sur une grille 8x8 (64 cases) soumise à plusieurs contraintes:

- Un chiffre par case
- Un chiffre doit être entouré de chiffres différents (y compris en diagonale)
- Un motif de N cases (repéré en traits gras) doit comporter tous les chiffres de 1 à N

## Architecture — MVC

**Architecture approximative**

```
Neonaure
├── assets
│   └── misc
│       └── images
│ 
├── controller
│   ├── controller.py
│   └── __init__.py
│ 
├── view
│   ├── main_window.py
│   └── __init__.py
│
├── examples
│   ├── grille1.json
│   ├── grille2.json
│   ├── grille3.json
│   ├── grille4.json
│   ├── grille5.json
│   ├── grille6.json
│   ├── grille7.json
│   ├── grille8.json
│   └── grille9.json
├── functools
│   └── json_handler.py
├── main.py
└── README.md
```

## Équipe

| Nom       | Prénom | Groupe TP |
| :-------- | :----: | --------: |
| DELPLACE  |  Hugo  |         E |
| DUFOUR    | Arthur |         E |
| MORMENTYN |  Noa   |         D |

## Enseignants

- Responsable : **L. Conoir**
- Intervenants : **R. Cozot**, **J. Hermilier**

<br>
<hr color = "red">

<p align="center">
  <img src="assets/misc/images/iutlittoral-logo.png" height="100" title="IUT">
  <img src="assets/misc/images/Logo_Université_du_Littoral_Côte_d'Opale.png" height="100" title="ULCO">
</p>
