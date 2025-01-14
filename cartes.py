import random

class Carte:
    """
    Une carte UNO.

    Paramètres:
        couleur (str): La couleur de la carte
        valeur (str): La valeur de la carte
    """

    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur

class Paquet:
    """
    Un paquet de cartes UNO comportant 108 cartes.
    """

    def __init__(self):
        self.cartes = []

        for n in range(4):
            pass
            #self.cartes.append( Carte('special', '4 couleur') )
            #self.cartes.append( Carte('special', 'prendre 4') )
        
        for couleur in ('rouge', 'jaune', 'vert', 'bleu'):
            self.cartes.append( Carte(couleur, 0) )
            
            # Deux fois
            for n in range(2):
                for numero in range(1, 10):
                    self.cartes.append( Carte(couleur, numero) )
                    
                # Cartes spéciaux
                self.cartes.append( Carte(couleur, 'skip') )
                self.cartes.append( Carte(couleur, 'inverse') )
                #self.cartes.append( Carte(couleur, 'prendre 2') )

        random.shuffle(self.cartes)

        # Pour qu'on n'ait pas une carte "special" au dessus
        while self.top().couleur == 'special' or self.top().valeur == 'prendre 2':
            random.shuffle(self.cartes)

    def top(self):
        """
        Lire la carte au dessus du paquet.

        Retour (Carte): La carte au dessus.
        """
        return self.cartes[0]
        
    def piocher(self):
        """
        Prendre une carte du paquet.

        Retour (Carte): La carte piochée.
        """

        index = random.randint(1, len(self.cartes)-1)
        return self.cartes.pop(index)
    
    def piocher_n(self, n_cartes):
        """
        Piocher n_cartes cartes du paquet.

        Retour (list): Les cartes piochées.
        """

        cartes = []
        for n in range(n_cartes):
            cartes.append(self.piocher())
        
        return cartes
    
    def deposer(self, carte):
        """
        Jouer une carte.

        Paramètres:
            carte (Carte): La carte à jouer.
        """

        self.cartes.insert(0, carte)