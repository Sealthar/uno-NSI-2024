# Jeu NSI 2024
# Collaborateurs: Rayan, Lothar, Robert

import random
import copy
import pyxel
import math

class Carte:
    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur
        
    def __repr__(self):
        return f'(carte {self.couleur} "{self.valeur}")'


class Paquet:
    def __init__(self):
        self.cartes = []
        
        for couleur in ('rouge', 'jaune', 'vert', 'bleu'):
            self.cartes.append( Carte(couleur, 0) )
            #self.cartes.append( Carte('special', '4 couleur') )
           # self.cartes.append( Carte('special', 'prendre 4') )
            
            # Deux fois
            for n in range(2):
                for numero in range(1, 10):
                    self.cartes.append( Carte(couleur, numero) )
                    
                # Cartes spéciaux
                #self.cartes.append( Carte(couleur, 'skip') )
                #self.cartes.append( Carte(couleur, 'inverse') )
                #self.cartes.append( Carte(couleur, 'prendre 2') )
        
        random.shuffle(self.cartes)
        
        self.carte_dessus = self.prendre()
        while self.carte_dessus.couleur == 'special' or self.carte_dessus.valeur == 'prendre 2':
            self.deposer(self.carte_dessus)
            self.carte_dessus = self.prendre()
        
    def prendre(self, n_cartes=1):
        if n_cartes == 1:
            return self.cartes.pop()
        else:
            cartes = []
            for i in range(n_cartes):
                cartes.append(self.cartes.pop())
            return cartes
        
    def deposer(self, carte):
        idx = random.randint(0, len(self.cartes))
        self.cartes.insert(idx, self.carte_dessus)
        self.carte_dessus = carte


class MainJoueur:
    def __init__(self, paquet):
        self.paquet = paquet
        self.main = self.paquet.prendre(7)
        
    def lister(self):
        print('> Main:')
        i = 0
        for carte in self.main:
            i += 1
            print(f'> [{i}] {carte}')
    
    def prendre(self, n=1):
        if n == 1:
            self.main.append(self.paquet.prendre(n))
        else:
            self.main += self.paquet.prendre(n)
            
        
    def ajouter(self, carte):
        self.main.append(carte)
        
    def lire(self, n):
        return self.main[n]
    
    def jouer(self, n):
        self.paquet.deposer(self.main.pop(n))
        
    def __len__(self):
        return len(self.main)
    

class JeuUno:
    def __init__(self):
        self.paquet = Paquet()
        self.main_joueurs = []
        for n in range(2):
            main = MainJoueur(self.paquet)
            self.main_joueurs.append(main)

        self.current_hand_pos = 0
        self.position = 0
        self.fin = False

        pyxel.init(128, 256)
        pyxel.load('res.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q) or self.fin == True:
            pyxel.quit()

    def draw(self):
        main = self.main_joueurs[self.position]

        pyxel.cls(1)
        pyxel.text(14, 16, f"C'est le tour du Joueur {self.position+1}", col=7)

        self.draw_buttons()
        card = self.draw_cards(self.paquet.carte_dessus, main)
        self.draw_cursor() 

        if card != None:
            print('tour de joueur', self.position+1)

            bonne_entree = False

            if card == -1:
                print('passer. prise de 1')
                main.prendre()
                bonne_entree = True
            else:
                carte = main.lire(card)
                carte_dessus = self.paquet.carte_dessus

                if carte_dessus.couleur == carte.couleur or carte_dessus.valeur == carte.valeur:
                    main.jouer(card)
                    print(f'vous avez joué {carte}')
                    bonne_entree = True
            
            if bonne_entree:
                self.current_hand_pos = 0
                self.position = (self.position+1) % 2
                if len(main) == 0:
                    print(f'Joueur {self.position+1} vous avez gagné!!')
                    self.fin = True

            else:
                print('mauvaise entrée')



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
        for card in hand.main[self.current_hand_pos*5:min((self.current_hand_pos*5)+5, len(hand))]:
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