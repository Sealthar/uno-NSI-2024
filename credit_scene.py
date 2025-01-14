from graphics import Scene, Sprite, GraphicSprite, CursorSprite

import pyxel
import time

class CreditText(Sprite):
    TEXT = """
=== CREDITS ===

Rayan: Pixel art, support moral
Lothar: Programmation
Robert: Programmation
Carlos: Artist
M. Georges-St. Marc: Prof

===============
"""
    def __init__(self):
        super().__init__()
        
        self.y = 256

    def draw(self):
        pyxel.text(4, self.y, self.TEXT, col=7)
        self.y -=1

class SceneCredits(Scene):
    def __init__(self):
        super().__init__()

        self.sprites.append( CreditText() )
        self.sprites.append( CursorSprite() )

    def draw(self):
        super().draw()

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.game_manager.current_scene = 0