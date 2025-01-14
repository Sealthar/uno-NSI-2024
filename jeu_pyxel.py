# Jeu UNO
# Classe de 1NSI 2024
# Collaborateurs: Rayan, Lothar, Robert

import pyxel
import math

from cartes import Carte, Paquet


class JeuUno:
    def __init__(self):
        self.paquet = Paquet()

        self.joueurs = []
        for n in range(2):
            main = self.paquet.piocher_n(7)
            self.joueurs.append(main)

        self.current_hand_pos = 0
        self.position = 0
        self.fin = False
        self.special_prochain = None

        self.popup_queue = []

        pyxel.init(128, 256)
        pyxel.load('res.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q) or self.fin == True:
            pyxel.quit()

    def draw(self):
        main = self.joueurs[self.position]

        if len(self.popup_queue) == 0:
            pyxel.cls(1)
        else:
            self.draw_scroll_bg()
            self.draw_centered_text(self.popup_queue[0])
            self.draw_cursor()

            if self.popup_queue[0] == 'Saut de tour, desole...':
                self.position = (self.position+1) % 2

            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.show_screen = False
                self.popup_queue.pop(0)
            return
        
        pyxel.text(14, 16, f"C'est le tour du Joueur {self.position+1}", col=7)

        self.draw_buttons()
        carte_choisi_index = self.draw_cards(top_card=self.paquet.top(), hand=main)
        self.draw_cursor() 

        if carte_choisi_index != None:
            bonne_entree = False

            if carte_choisi_index == -1:
                # "pass"
                main.append(self.paquet.piocher())
                bonne_entree = True
            else:
                carte_choisi = main[carte_choisi_index]
                carte_dessus = self.paquet.top()

                if carte_dessus.couleur == carte_choisi.couleur or carte_dessus.valeur == carte_choisi.valeur:
                    self.paquet.deposer(main.pop(carte_choisi_index))
                    bonne_entree = True

                    if carte_choisi.valeur in ('skip', 'inverse'):
                        self.popup_queue.append('Saut de tour, desole...')
            
            if bonne_entree:
                if len(main) == 0:
                    self.fin = True
                else:
                    self.popup_queue.insert(0, f"C'est le tour du joueur {((self.position+1) % 2) + 1}")
                
                self.current_hand_pos = 0
                self.position = (self.position+1) % 2

    def draw_centered_text(self, text, y=125, col=7):
        pyxel.text(64-2*len(text), y, text, col)


    def draw_scroll_bg(self):
        i = (pyxel.frame_count // 2) % 4
        u = 64 + (i % 2)*8
        v = 80 + (i // 2)*8
        for y in range(0, 257, 16):
            for x in range(0, 129, 16):
                pyxel.blt(x, y, 0, u, v, 8, 8, scale=2)

    def draw_buttons(self):
        pyxel.blt(100, 100, 0, u=32, v=80, w=16, h=16, colkey=15, scale=2)
        pyxel.blt(100, 124, 0, u=16, v=80, w=16, h=16, colkey=15, scale=2)

    def draw_cards(self, top_card, hand):
    # top
        self.draw_card(20, 112, top_card)
        pyxel.blt(60, 112, 0, u=48, v=64, w=16, h=16, colkey=15, scale=2)

        MAX_HAND = math.ceil(len(hand)/5)
        pyxel.text(56, 184, str(self.current_hand_pos + 1) + '/' + str(MAX_HAND), 7)

        card_played = None

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.current_hand_pos -= 1
            if self.current_hand_pos < 0:
                self.current_hand_pos = MAX_HAND-1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.current_hand_pos += 1
            if self.current_hand_pos >= MAX_HAND:
                self.current_hand_pos = 0
        elif pyxel.btnp(pyxel.KEY_1):
            card_played = self.current_hand_pos*5
        elif pyxel.btnp(pyxel.KEY_2):
            card_played = self.current_hand_pos*5 + 1
        elif pyxel.btnp(pyxel.KEY_3):
            card_played = self.current_hand_pos*5 + 2
        elif pyxel.btnp(pyxel.KEY_4):
            card_played = self.current_hand_pos*5 + 3
        elif pyxel.btnp(pyxel.KEY_5):
            card_played = self.current_hand_pos*5 + 4
        elif pyxel.btnp(pyxel.KEY_RETURN):
            card_played = -1
            pass

        if card_played != None:
            if card_played >= len(hand):
                card_played = None
        
        # bottom
        i = 16
        for card in hand[self.current_hand_pos*5:min((self.current_hand_pos*5)+5, len(hand))]:
            self.draw_card(i, 200, card)
            i += 20

        # arrows
        pyxel.blt(2, 200, 0, u=64, v=64, w=4, h=14, colkey=0, scale=1)
        pyxel.blt(122, 200, 0, u=68, v=64, w=4, h=14, colkey=0, scale=1)

        return card_played

    def draw_cursor(self):
        pyxel.blt(pyxel.mouse_x-4, pyxel.mouse_y-2, 0, u=48, v=80, w=16, h=16, colkey=15, scale=1)

    def draw_card(self, x, y, card):
        if card.couleur == 'special' and card.valeur == 'prendre 4':
            u = 0
            v = 64
        elif card.couleur == 'special' and card.valeur == '4 couleur':
            u = 16
            v = 64
        else:
            if card.valeur == 'skip':
                u = 160
            elif card.valeur == 'inverse':
                u = 176
            elif card.valeur == 'prendre 2':
                u = 192
            else:
                u = card.valeur * 16   

            if card.couleur == 'rouge':
                v = 0
            elif card.couleur == 'jaune':
                v = 16
            elif card.couleur == 'vert':
                v = 32
            elif card.couleur == 'bleu':
                v = 48

        pyxel.blt(x, y, 0, u, v, w=16, h=16, colkey=15, scale=2)


app = JeuUno()