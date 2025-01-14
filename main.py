from init_scene import SceneInit
from transition_scene import SceneTransition
from uno_scene import SceneUno
from graphics import GameManager

scenes = [SceneInit(), SceneUno(), SceneTransition(1), SceneTransition(2)]
game = GameManager(scenes)