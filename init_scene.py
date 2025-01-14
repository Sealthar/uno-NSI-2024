from graphics import Scene, ButtonSprite, CursorSprite

class BeginButton(ButtonSprite):
    def __init__(self):
        super().__init__(64-8, 128-8, 0, 80, 16, 16, scale=2)
    
    def on_click(self):
        self.game_manager.current_scene = 1

class SceneInit(Scene):
    def __init__(self):
        super().__init__()

        self.sprites.append( BeginButton() )
        self.sprites.append( CursorSprite() )