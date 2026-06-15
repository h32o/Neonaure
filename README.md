# SAÉ Graphes-IHM — Néonaure

## Présentation

Le **Néonaure** est inspiré du Sudoku joué généralement sur une grille 8x8 (64 cases) soumise à plusieurs contraintes:

- Un chiffre par case
- Un chiffre doit être entouré de chiffres différents (y compris en diagonale)
- Un motif de N cases (repéré en traits gras) doit comporter tous les chiffres de 1 à N

## Fonctionnalité de l'application

### Jeu & Gameplay
- **Menu d'accueil interactif** : Permet de lancer une partie, de configurer ou de quitter proprement l'application.
- **Grille interactive** : Saisie et modification intuitive des chiffres dans la grille de jeu, avec distinction visuelle claire entre les chiffres de départ (lecture seule) et ceux saisis par le joueur.
- **Détection d'erreurs en temps réel** : Surlignage visuel (rouge) des cases en conflit(cases adjacentes identiques) ou de motifs.
- **Historique complet (Undo / Redo)** : Possibilité d'annuler (`Ctrl+Z`) ou de rétablir (`Ctrl+Y`) toutes vos actions à tout moment.
- **Générateur de grilles personnalisé** : Permet de concevoir des grilles sur mesure en spécifiant le nombre de lignes (de 4 à 12), de colonnes (de 4 à 12) et le pourcentage de cases initialement dévoilées.
- **Chargement & Sauvegarde** : Exportez vos grilles ou chargez-en de nouvelles au format JSON (`Ctrl+S` / `Ctrl+L`).

### Intelligence Artificielle & Aide
- **Solveur automatique** : Résolution complète et instantanée de la grille de jeu à l'aide d'un algorithme de backtracking.
- **Système d'indices (Hint)** : Aide ponctuelle via le bouton d'indice (ampoule) qui révèle une case correcte, avec un système de temps de recharge (cooldown) de 60 secondes pour préserver le défi.

### Paramètres & Personnalisation
- **Panneau latéral de paramètres** : Menu glissant et animé donnant accès aux réglages de l'application.
- **Profil utilisateur** : Personnalisation et enregistrement d'un pseudonyme affiché à l'écran de jeu.
- **Options d'affichage** : Activation/désactivation de l'affichage du chronomètre de jeu.
- **Règles intégrées** : Accès rapide aux règles détaillées du Néonaure directement dans l'interface.


## Architecture — MVC

**Architecture approximative**

```
Neonaure
├── assets
│   └── misc
│       └── images
├── controller
│   ├── controller.py
│   └── __init__.py
├── examples
│   ├── grille1.json
│   ├── grille2.json
│   ├── grille3.json
│   ├── grille4.json
│   ├── grille5.json
│   ├── grille6.json
│   ├── grille7.json
│   ├── grille8.json
│   └── grille9.json
├── model
│   ├── Cell.py
│   ├── Grid_Generator.py
│   ├── Grid.py
│   ├── __init__.py
│   ├── Pattern.py
│   └── solveur.py
├── tools
│   └── json_handler.py
├── view
│   ├── components
│   │   ├── cell_widget.py
│   │   └── grid_widget.py
│   ├── __init__.py
│   ├── main_window.py
│   ├── menu_window.py
│   └── settings_window.py
├── .gitignore
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
<hr style="border: none; height: 1px; background-color: red; border-top: 1px solid red;">

<p align="center">
  <img src="assets/misc/images/iutlittoral-logo.png" height="100" title="IUT">
  <img src="assets/misc/images/Logo_Université_du_Littoral_Côte_d'Opale.png" height="100" title="ULCO">
</p>
