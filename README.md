# Learn2Slither

Projet réalisé dans le cadre du cursus post tronc commun de l'école 42 Angoulême.

---

## Description

Learn2Slither est un projet d'apprentissage par renforcement dont l'objectif est d'entraîner un agent IA à jouer au jeu Snake de manière autonome.

L'agent apprend par essais et erreurs en interagissant avec son environnement. À chaque action effectuée, il reçoit une récompense ou une pénalité lui permettant d'améliorer progressivement sa stratégie grâce à l'algorithme de Q-Learning.

## Stack & Architecture

| Technologie | Utilisation |
|------------|-------------|
| Python | Langage principal du projet |
| Pygame | Gestion du rendu graphique et des interactions |
| Pandas | Analyse et traitement des statistiques d'entraînement |
| Q-Learning | Algorithme d'apprentissage par renforcement basé sur l'équation de Bellman |

```bash
.
├── ai
│   ├── Qlearning_agent.py
│   └── snake_agent.py
├── assets
│   ├── GameSettings.png
│   ├── GameStats.png
│   ├── IASettings.png
│   ├── Menu.png
│   ├── PressStart2P-Regular.ttf
│   └── Snake.png
├── controllers
│   ├── agent_controller.py
│   └── human_controller.py
├── game
│   ├── apple.py
│   ├── snake.py
│   ├── snake_env.py
│   └── state.py
├── models
│   ├── q_table_10.pkl
│   ├── q_table_100.pkl
│   ├── q_table_1000.pkl
│   ├── q_table_10000.pkl
│   ├── q_table_20000.pkl
│   └── q_table_error.pkl
├── render
│   ├── button_render.py
│   ├── game_render.py
│   └── popup_render.py
├── scenes
│   ├── agent_scene.py
│   ├── ai_settings_scene.py
│   ├── game_settings_scene.py
│   ├── human_scene.py
│   ├── mainmenu_scene.py
│   ├── scene.py
│   └── stats_scene.py
├── stats
│   └── manage_csv.py
├── app.py
├── config.py
├── const.py
├── parser.py
├── README.md
└── requirements.txt

```


## Installation

```bash
python3 -m venv .venv
pip install -r requirements.txt
```

## Lancement de l'agent

```bash
❯ python app.py -h    
usage: app.py [-h] [-sessions SESSIONS] [-save SAVE] [-visual {on,off}] [-load LOAD] [-dontlearn] [-step_by_step] [-human]

A snake that learns how to behave in an environment through trial and error, using the Q-learning algorithm.

options:
  -h, --help          show this help message and exit
  -sessions SESSIONS  Number of training sessions for the snake agent.
  -save, -s SAVE      Name of model file to be saved.
  -visual {on,off}    Enable visual mode to see the snake learning in real-time.
  -load LOAD          Name of the model to be loaded.
  -dontlearn          Disable learning mode for the snake agent.
  -step_by_step       Enable step-by-step learning mode.
  -human              Play the game as a human player.
```

---

## Q-Learning

Le Q-Learning est un algorithme d'apprentissage par renforcement permettant à un agent d'apprendre une politique optimale sans connaissance préalable de l'environnement.

L'algorithme repose sur l'équation de Bellman :

```python
Q(s, a) = Q(s, a) + α × (reward + γ × max(Q(s', a')) − Q(s, a))
```
où :
- **s** : état courant
- **a** : action effectuée
- **reward** : récompense obtenue
- **s'** : nouvel état
- **α** : taux d'apprentissage (*learning rate*)
- **γ** : facteur de réduction (*discount factor*)

L'objectif est de construire une **Q-table** contenant une estimation de la qualité de chaque action pour chaque état rencontré :

```python
q_table[state] = {
    "UP": value,
    "DOWN": value,
    "LEFT": value,
    "RIGHT": value
}
```

### Choix du state


**Conception de l'espace d'états**

La principale difficulté du Q-Learning consiste à définir un état suffisamment descriptif pour permettre à l'agent de prendre de bonnes décisions tout en conservant un espace d'états raisonnable.

Un état trop simple entraîne une perte d'informations importantes.

Un état trop complexe augmente fortement le nombre de combinaisons possibles et ralentit l'apprentissage.

**Ordre de grandeur**

| Taille de l'espace d'états | Convergence |
|---------------------------|-------------|
| < 10 000 | Rapide |
| 10 000 – 100 000 | Acceptable |
| > 1 000 000 | Q-Learning tabulaire peu adapté |

> Un bon état encode uniquement les informations nécessaires à la prise de décision. Il doit maximiser la pertinence tout en minimisant le nombre de combinaisons possibles.

**Malédiction de la dimensionnalité**

Chaque variable ajoutée multiplie le nombre total d'états :

```text
4 dangers (booléens)  ->      16 états
+ direction           ->      64 états
+ position exacte     ->   64 000 états
```

### Mon state

**État utilisé dans Learn2Slither**

L'état retenu encode :

- les dangers immédiats autour de la tête ;
- la direction actuelle du serpent ;
- une vision simplifiée dans les quatre directions cardinales:
  - Premier élément rencontré dans la direction
  - W , G , R
  - S est considéré comme W
  - R si snake.size() <= 2 est considéré comme W

### Décomposition

| Composant | Combinaisons |
|-----------|-------------|
| Dangers (4 booléens) | 2⁴ = 16 |
| Direction courante | 4 |
| Vision simplifiée (4 directions, 3 valeurs possibles) | 3⁴ = 81 |
| **Total** | **5 184 états** |

### Exemple

```python
State(
    danger=(False, True, False, True),
    direction=(-1, 0),
    up="W",
    down="W",
    right="W",
    left="W"
)

Valeur {'UP': 0.0, 'DOWN': 0.0, 'LEFT': 0.0, 'RIGHT': 0.0}
```

**Récompenses**

L'agent reçoit des récompenses afin d'orienter son apprentissage :

| Événement | Récompense |
|-----------|------------|
| Consommation d'une pomme verte | +10 |
| Consommation d'une pomme rouge | -5|
| Consommation d'une pomme rouge si trop petit | -10|
| Survie d'un tour | -0.01 |
| Passage à une taille 0 |-100 |
| Collision avec un mur | -100 |
| Collision avec lui-même | -100 |

Ces récompenses permettent à l'agent d'apprendre progressivement les comportements favorables à sa survie et à l'obtention d'un score élevé.

## Aperçu du jeu

<img src="assets/Menu.png" alt="A floating image" style="width: 300px; float: left; margin-left: 15px;">
<img src="assets/GameSettings.png" alt="A floating image" style="width: 300px; float: left; margin-left: 15px;">
<img src="assets/IASettings.png" alt="A floating image" style="width: 300px; float: left; margin-left: 15px;">
<img src="assets/Snake.png" alt="A floating image" style="width: 300px; float: left; margin-left: 15px;">
<img src="assets/GameStats.png" alt="A floating image" style="width: 300px; float: left; margin-left: 15px;">


