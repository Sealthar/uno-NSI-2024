from graphics import Scene, ButtonSprite, CursorSprite

import pyxel

class BeginButton(ButtonSprite):
    def __init__(self):
        super().__init__(64-8, 128-24-8, 0, 80, 16, 16, scale=2)
    
    def on_click(self):
        self.game_manager.current_scene = 1

class CreditsButton(ButtonSprite):
    def __init__(self):
        super().__init__(64-8, 128+24-8, 32, 128, 16, 16, scale=2)
    
    def on_click(self):
        self.game_manager.current_scene = 1

class SceneInit(Scene):
    def __init__(self):
        super().__init__()

        self.sprites.append( BeginButton() )
        self.sprites.append( CreditsButton() )
        self.sprites.append( CursorSprite() )

    def draw(self):
        super().draw()

        pyxel.text(42, 60, 'Jeu UNO NSI', 7)