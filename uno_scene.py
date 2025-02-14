from cartes import Paquet
from graphics import Scene, ButtonSprite, CursorSprite, GraphicSprite, Sprite

import pyxel


class PlayerText(Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.x = x
        self.y = y
        self.turn = 0

    def draw(self):
        pyxel.text(self.x, self.y, f"C'est le tour du Joueur {self.turn+1}", col=7)

class UnoButton(ButtonSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 80, 16, 16, scale=2)

class SkipButton(ButtonSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 80, 16, 16, scale=2)
        self.clicked = False

    def on_click(self):
        self.clicked = True

class DiscardPile(GraphicSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 64, 16, 16, scale=2)

class GraphicCard(GraphicSprite):
    def __init__(self, x, y, bobbles=True):
        super().__init__(x, y, 0, 0, 16, 16, scale=2)

        self.mouse_last_x = 0
        self.mouse_last_y = 0
        self.card = None
        self.selected = False
        self.bobbles = bobbles

    def set_card(self, card):
        self.card = card

        if card.couleur == 'special' and card.valeur == 'prendre 4':
            self.u = 0
            self.v = 64
        elif card.couleur == 'special' and card.valeur == '4 couleur':
            self.u = 16
            self.v = 64
        else:
            if card.valeur == 'skip':
                self.u = 160
            elif card.valeur == 'inverse':
                self.u = 176
            elif card.valeur == 'prendre 2':
                self.u = 192
            else:
                self.u = card.valeur * 16   

            if card.couleur == 'rouge':
                self.v = 0
            elif card.couleur == 'jaune':
                self.v = 16
            elif card.couleur == 'vert':
                self.v = 32
            elif card.couleur == 'bleu':
                self.v = 48

    def draw(self):
        self.selected = False

        x = self.x - (self.w // 2)
        y = self.y - (self.h // 2)
        w = self.w * self.scale
        h = self.h * self.scale

        if x <= pyxel.mouse_x <= x+w and y <= pyxel.mouse_y <= y+h and self.bobbles:
            self.y -= 6
            super().draw()
            self.y += 6
        else:
            super().draw()

        if x <= pyxel.mouse_x <= x+w and y <= pyxel.mouse_y <= y+h:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.mouse_last_x = pyxel.mouse_x
                self.mouse_last_y = pyxel.mouse_y
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                if pyxel.mouse_x == self.mouse_last_x and pyxel.mouse_y == self.mouse_last_y:
                    self.selected = True

class GraphicHand(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        
        self.min_x = x
        self.max_x = x
        self.last_mouse_x = 0

        self.cards = []

        self.selected_card = None
    
    def set_hand(self, hand):
        self.cards = []
        for card in hand:
            graphic_card = GraphicCard(0, self.y)
            graphic_card.set_card(card)
            self.cards.append(graphic_card)

        cards_width = 36*len(hand) + 14 - 128
        self.min_x = self.max_x - cards_width
        self.x = self.max_x

    def draw(self):
        self.selected_card = None

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y >= self.y:
            self.last_mouse_x = pyxel.mouse_x
           
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y >= self.y:
            self.x += pyxel.mouse_x - self.last_mouse_x
            self.last_mouse_x = pyxel.mouse_x

            if self.x > self.max_x:
                self.x = self.max_x
            elif self.x < self.min_x:
                self.x = self.min_x
        
        x = self.x
        i = 0

        for card in self.cards:
            card.x = x
            card.draw()

            if card.selected:
                self.selected_card = i

            x += 36
            i += 1

            

    def update(self):
        for card in self.cards:
            card.update()

class SwapHandsGraphic(GraphicSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 112, 16, 16, scale=4)
        self.timer = 60
        self.type = None

    def draw(self):
        if self.type == 'prendre 2':
            self.u = 16
            self.v = 96
        elif self.type == 'skip':
            self.u = 32
            self.v = 112

        super().draw()
        pyxel.blt(self.x, self.y + ((pyxel.frame_count // 5) % 4) * 4, 0, 48, 112, 16, 16, colkey=15, scale=4)
        self.timer -= 1

class SceneUno(Scene):
    def __init__(self):
        super().__init__()

        self.paquet = Paquet()

        self.joueurs = []
        for n in range(2):
            main = self.paquet.piocher_n(7)
            self.joueurs.append(main)

        self.tour = 0
        self.avant_action = None
        self.update_hand = True

        self.graphic_hand = GraphicHand(16, 200)
        self.top_graphic_card = GraphicCard(20, 112, bobbles=False)
        self.discard_pile = DiscardPile(60, 112)
        #self.uno_button = UnoButton(100, 100)
        #self.skip_button = SkipButton(100, 124)
        self.skip_button = SkipButton(100, 112)
        self.player_text = PlayerText(14, 16)
        self.swap_hands = SwapHandsGraphic(64-8, 128-8)
        self.swap_hands.visible = False

        self.sprites.append(self.graphic_hand)
        self.sprites.append(self.top_graphic_card)
        self.sprites.append(self.discard_pile)
        #self.sprites.append(self.uno_button)
        self.sprites.append(self.skip_button)
        self.sprites.append(self.player_text)
        self.sprites.append(self.swap_hands)
        self.sprites.append( CursorSprite() )

    def draw(self):
        hand = self.joueurs[self.tour]

        if self.update_hand:
            self.graphic_hand.set_hand(hand)
        self.update_hand = False

        self.top_graphic_card.set_card(self.paquet.top())
        self.player_text.turn = self.tour
        super().draw()

        bonne_entree = False

        if self.avant_action in ('skip', 'prendre 2'):
            self.swap_hands.visible = True
            self.swap_hands.type = self.avant_action

            if self.swap_hands.timer < 0:
                self.swap_hands.visible = False
                self.swap_hands.timer = 60
                
                if self.avant_action == 'skip':
                    bonne_entree = True
                elif self.avant_action == 'prendre 2':
                    for carte in self.paquet.piocher_n(2):
                        hand.append(carte)
                        self.update_hand = True

                self.avant_action = None

        if self.skip_button.clicked and not bonne_entree:
            self.avant_action = None

            self.skip_button.clicked = False
            hand.append(self.paquet.piocher())
            bonne_entree = True

        if self.graphic_hand.selected_card != None and not bonne_entree:
            self.avant_action = None
            
            carte_index = self.graphic_hand.selected_card
            carte_choisi = hand[carte_index]
            carte_dessus = self.paquet.top()

            if carte_dessus.couleur == carte_choisi.couleur or carte_dessus.valeur == carte_choisi.valeur:
                self.paquet.deposer(hand.pop(carte_index))

                if carte_choisi.valeur in ('skip', 'inverse'):                    
                    self.avant_action = 'skip'
                elif carte_choisi.valeur == 'prendre 2':
                    self.avant_action = 'prendre 2'
                
                bonne_entree = True

        if bonne_entree:
            self.tour = (self.tour + 1) % 2
            self.game_manager.current_scene = self.tour + 2
            self.update_hand = True

