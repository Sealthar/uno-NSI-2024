# Jeu NSI 2024
# Collaborateurs: Rayan, Lothar, Robert

import random
import copy
import pyxel

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
            self.cartes.append( Carte('special', '4 couleur') )
            self.cartes.append( Carte('special', 'prendre 4') )
            
            # Deux fois
            for n in range(2):
                for numero in range(1, 10):
                    self.cartes.append( Carte(couleur, numero) )
                    
                # Cartes spéciaux
                self.cartes.append( Carte(couleur, 'skip') )
                self.cartes.append( Carte(couleur, 'inverse') )
                self.cartes.append( Carte(couleur, 'prendre 2') )
        
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
    

class App:
    def __init__(self):
        #deleteme
        self.hand = Paquet().prendre(7)

        pyxel.init(128, 256)
        pyxel.load('res.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(1)
        pyxel.text(14, 16, 'C\'est le tour du Joueur 1', col=7)
        self.draw_buttons()
        self.draw_cards()
        self.draw_cursor()

    def draw_buttons(self):
        pyxel.blt(100, 100, 0, u=32, v=80, w=16, h=16, colkey=15, scale=2)
        pyxel.blt(100, 124, 0, u=16, v=80, w=16, h=16, colkey=15, scale=2)

    def draw_cards(self):
    # top
        pyxel.blt(20, 112, 0, u=0, v=0, w=16, h=16, colkey=15, scale=2)
        pyxel.blt(60, 112, 0, u=48, v=64, w=16, h=16, colkey=15, scale=2)

        # bottom
        i = 16
        for card in self.hand[:5]:
            self.draw_card(i, 200, card)
            i += 20

        # arrows
        pyxel.blt(2, 200, 0, u=64, v=64, w=4, h=14, colkey=0, scale=1)
        pyxel.blt(122, 200, 0, u=68, v=64, w=4, h=14, colkey=0, scale=1)

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


app = App()