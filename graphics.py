import pyxel

class Scene:
    """
    Une scène qui peut contenir des sprites.

    Paramètres:
        bg_color (int, optionnel): Couleur du fond.
    """

    def __init__(self, bg_color=1):
        self.sprites = []
        self.bg_color = bg_color

    def draw(self):

        pyxel.cls(self.bg_color)
        for sprite in self.sprites:
            sprite.game_manager = self.game_manager
            sprite.draw()
    
    def update(self):
        for sprite in self.sprites:
            sprite.update()

class GameManager:
    """
    Gérant des scènes. Contient un ou plusieurs scènes.
    La première scène qui sera affichée c'est celui à l'indice 0.

    Paramètres:
        scenes (list): Une liste en scènes.
    """

    def __init__(self, scenes):
        pyxel.init(128, 256)
        pyxel.load('res.pyxres')

        self.scenes = scenes
        self.current_scene = 0
        self.end = False

        for scene in self.scenes:
            scene.game_manager = self

        pyxel.run(self.update, self.draw)

    def draw(self):
        self.scenes[self.current_scene].draw()

    def update(self):
        self.scenes[self.current_scene].update()

        if pyxel.btnp(pyxel.KEY_Q) or self.end == True:
            pyxel.quit()

class Sprite:
    """
    Classe de base pour un sprite générique. Sans utilité sauf pour sous-classer.
    """

    def __init__(self):
        pass

    def draw(self):
        """
        Logique pour dessiner le sprite. Il est possible d'ajouter de la fonctionnalité en
        créant une classe fille et outre-passant la fonction, par exemple:
        
        class AutreSprite(Sprite):
            [...]
            def draw(self):
                [...]
                super().draw()
        """

        pass

    def update(self):
        """
        Logique pour actualiser le sprite. Il est possible d'ajouter de la fonctionnalité en
        créant une classe fille et outre-passant la fonction, par exemple:
        
        class AutreSprite(Sprite):
            [...]
            def draw(self):
                [...]
                super().draw()
        """

        pass

class GraphicSprite(Sprite):
    """
    Classe pour un sprite graphique.

    Paramètres:
        x, y (int): Position du sprite dans la scène.
        u, v (int): Position du sprite dans la banque d'image.
        w, h (int): Largeur et lonugeur du sprite.
        colkey (int, optionnel): Couleur qui sera "transparente", celle-ci défaut à 15.
        scale (int, optionnel): L'échelle du sprite.

    """

    def __init__(self, x, y, u, v, w, h, colkey=15, scale=1):
        self.x, self.y = x, y
        self.u, self.v = u, v
        self.w, self.h = w, h
        self.scale = scale
        self.colkey = colkey

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, colkey=self.colkey, scale=self.scale)

class ButtonSprite(GraphicSprite):
    """
    Classe de bouton qui peut recevoir des entrées de souris.

    Paramètres:
        x, y (int): Position du sprite dans la scène.
        u, v (int): Position du sprite dans la banque d'image.
        w, h (int): Largeur et lonugeur du sprite.
        colkey (int, optionnel): Couleur qui sera "transparente", celle-ci défaut à 15.
        scale (int, optionnel): L'échelle du sprite.

    """

    def draw(self):
        x = self.x - (self.w // 2)
        y = self.y - (self.h // 2)
        w = self.w * self.scale
        h = self.h * self.scale


        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and \
           x <= pyxel.mouse_x <= x+w and \
           y <= pyxel.mouse_y <= y+h:
            
            self.on_click()

        
        super().draw()

    def on_click(self):
        """
        Cette fonction est appelée lorsque l'utilisateur fait un clic sur le sprite.
        Cette fonction doit être outre-passée.
        """

        pass

class CursorSprite(GraphicSprite):
    """
    Classe de curseur. Le curseur suivera la souris à chaque appel de draw().
    """

    def __init__(self):
        super().__init__(64, 128, u=48, v=80, w=16, h=16)

    def draw(self):
        self.x = pyxel.mouse_x-4
        self.y = pyxel.mouse_y-2

        super().draw()
