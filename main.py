from init_scene import SceneInit
from transition_scene import SceneTransition
from uno_scene import SceneUno
from credit_scene import SceneCredits
from graphics import GameManager

scenes = [SceneInit(), SceneUno(), SceneTransition(1), SceneTransition(2), SceneCredits()]
game = GameManager(scenes)