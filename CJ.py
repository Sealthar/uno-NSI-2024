import random
import time

elementalLoss = {'fire' : 'water',
                'water' : 'snow',
                'snow' : 'fire'}



class Card:
    def __init__(self, element, power, color, ability):
        self.element = element
        self.power = power
        self.color = color
        self.ability = ability
        

class Deck:
    def __init__(self, deck=None):
        self.deck = []
        if deck: self.deck = deck
            
    def shuffle(self):
        pass
    
    def newCard(self, element, power, color, ability):
        self.deck.append(Card(element, power, color, ability))

    def delCard(self, index):
        try: self.deck.pop(index)
        except: pass

class Player:
    
    def __init__(self, number, deck):
        self.number = number
        self.deck = deck
        self.hand = []
        self.selectedCards = []
        
    def draw(self):
        self.deck.insert(0, self.deck.pop())
        self.hand.append(self.deck[0])


def RCJstart(players):
    
    for player in players:
        
        player.deck.shuffle()

        for i in range(5):
            player.deck.draw()

def CJabilityCheck(players):
    

def regularCJbattle(players):
  
    activeAbilities = {'inverse': True,
                       'banned'}
  
    for player in players:
        
        
        
        if not CJabilityCheck(players)[player.number] == 1:
            if elementalLoss[player.selectedCards[0].element] == players[(players.index(player))-1].selectedCards[0].element:
                return players[(players.index(player))-1]


    for player in players:
        
        if player.selectedCards[0].power > players[(players.index(player))-1].selectedCards[0].power:
                return player
            return players[(players.index(player))-1]
    
    return 'tie'
    
def RCJscoredCard():
    
    

def regularCJ(player1, player2):
    
    players = [player1, player2]
    
    
    RCJstart(players)
    while not wincon:
        RCJcardSelect()
        RCJscoredCard(regularCJbattle(players))
        RCJwinCheck()
        
    RCJend()
        
    
    

        





