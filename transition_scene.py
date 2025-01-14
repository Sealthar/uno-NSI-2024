from graphics import Scene, Sprite, ButtonSprite, CursorSprite

import pyxel

class ScrollBackground(Sprite):
    def __init__(self):
        super().__init__(self)

    def draw(self):
        i = (pyxel.frame_count // 2) % 4
        u = 64 + (i % 2)*8
        v = 80 + (i // 2)*8
        for y in range(0, 257, 16):
            for x in range(0, 129, 16):
                pyxel.blt(x, y, 0, u, v, 8, 8, scale=2)

class PassPlayerText(Sprite):
    def __init__(self, x, y, joueur):
        super().__init__()
        self.x = x
        self.y = y
        self.joueur = joueur

    def draw(self):
        pyxel.text(self.x, self.y, f"C'est le tour du Joueur {self.joueur}", col=7)

class SceneTransition(Scene):
    def __init__(self, joueur):
        super().__init__()

        self.sprites.append( PassPlayerText(14, 127, joueur) )
        self.sprites.append( CursorSprite() )

    def draw(self):
        super().draw()

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.game_manager.current_scene = 1