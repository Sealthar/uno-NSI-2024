# Jeu NSI 2024
# Collaborateurs: Rayan, Lothar, Robert

import random
import copy

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
    

class JeuUno:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.joueurs_orig = joueurs
        self.position = 0
        self.ordre_inverse = False
        self.couleur_special_choisi = None
        self.action_special = None
        
        self.paquet = Paquet()
        
        self.main_joueurs = []
        for n in range(joueurs):
            main = MainJoueur(self.paquet)
            self.main_joueurs.append(main)
            
        while self.joueurs > 1:
            self.tour()
            
    def tour(self):
        print(f'>>> Tour du joueur {self.position+1}')
        main = self.main_joueurs[self.position]
        
        attention_on_garde_la_notice_couleur = False
        
        while True:
            override_couleur = None

            if self.action_special == 'skip' or (self.action_special == 'inverse' and self.joueurs == 2):
                print('Désolé, un joueur a sauté votre tour!')
                self.action_special = None
                break
            # we dont have +2 chaining sadly
            elif self.action_special == 'prendre 2':
                print('Vous prenez deux cartes!')
                main.prendre(2)
            elif self.action_special == 'prendre 4':
                print('Vous prenez quatre cartes!')
                main.prendre(4)
                print(f'La couleur est: {self.couleur_special_choisi}')
                override_couleur = self.couleur_special_choisi
            elif self.action_special == '4 couleur':
                print(f'La couleur est: {self.couleur_special_choisi}')
                override_couleur = self.couleur_special_choisi
            
            print(f'La carte au dessus: {self.paquet.carte_dessus}')
            main.lister()
            
            n = input('quelle carte veux-tu jouer (ou "passer")? ').strip()
            
            if n == 'passer':
                print('Vous avez pris 1 carte')
                main.prendre()
                
                if self.action_special in ('4 couleur', 'prendre 4'):
                    attention_on_garde_la_notice_couleur = True
                break
            
            if not n.isdigit():
                print('Mauvaise entrée')
                continue
            n = int(n)
            if n < 1 or n > len(main):
                print('Mauvaise entrée')
                continue
            
            idx = int(n) - 1
            carte = main.lire(idx)
            
            
            if self.paquet.carte_dessus.couleur != carte.couleur and \
               self.paquet.carte_dessus.valeur != carte.valeur and \
               override_couleur != carte.couleur and \
               carte.couleur != 'special':
                print("La carte n'est pas de la même couleur/nombre...")
                continue
            
            main.jouer(idx)
            print(f'vous avez joué {carte}')
            
            self.action_special = None
            
            if attention_on_garde_la_notice_couleur:
                self.action_special = '4 couleur'
            
            if carte.valeur in ('4 couleur', 'prendre 4', 'skip', 'inverse', 'prendre 2'):
                self.action_special = carte.valeur
            
            if carte.valeur == 'inverse':
                self.ordre_inverse = not self.ordre_inverse
                
            if carte.valeur in ('4 couleur', 'prendre 4'):
                while True:
                    self.couleur_special_choisi = input('Choisir le couleur de la carte (rouge,bleu,vert,jaune) ')
                    if self.couleur_special_choisi in ('rouge', 'jaune', 'vert', 'bleu'):
                        break
                    
            break
            
        if len(main) == 0:
            rang = self.joueurs_orig - self.joueurs + 1
            print(f'Joueur {self.position+1}, vous avez gagné en {rang}e place!!')
            self.joueurs -= 1
            self.main_joueurs.pop(self.position)
            
        print()
        print()
        
        if self.ordre_inverse:
            self.position -= 1
        else:
            self.position += 1
        self.position = self.position % self.joueurs
        
# note: des valeurs hors 2 marchent mais les numeros de joueurs changent (i.e. joueur 2 devient 1, 3 devient 2 ...)
jeu_uno = JeuUno(3)
