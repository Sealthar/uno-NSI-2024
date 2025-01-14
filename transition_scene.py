from graphics import Scene, Sprite, GraphicSprite, CursorSprite

import pyxel
import time

# class PassPlayerText(Sprite):
#     def __init__(self, x, y, joueur):
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.joueur = joueur

#     def draw(self):
#         pyxel.text(self.x, self.y, f"C'est le tour du Joueur {self.joueur}", col=7)

class NextPlayer(GraphicSprite):
    def __init__(self, x, y, player):
        if player == 1:
            u = 32
        else:
            u = 48
            
        super().__init__(x, y, u, 96, 16, 16, scale=4)

class SceneTransition(Scene):
    def __init__(self, joueur):
        super().__init__()

        self.sprites.append( NextPlayer(64-8, 128-8, joueur) )
        self.sprites.append( CursorSprite() )

    def draw(self):
        super().draw()

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.game_manager.current_scene = 1