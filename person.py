from random import shuffle
class Person:
  def __init__(self):
      self.hand = []
      
  def take_card(self, card):
      self.hand.append(card)
      
  def clear_hand(self):
      self.hand = []
      
  def calculate_hand(self):
      total = 0
      aces = 0
      for card in self.hand:
          if card in ['J', 'Q', 'K']:
              total += 10
          elif card == 'A':
              aces += 1
              total += 11
          else:
              total += card
      while total > 21 and aces:
          total -= 10
          aces -= 1
      return total

class Dealer(Person):
  def __init__(self):
    super().__init__()
    self.visible = False
    
  def __str__(self):
    if self.visible:
      return f"Dealer: {self.hand} (Total: {self.calculate_hand()})"
    return f"Dealer: [{self.hand[0]}, '?'] (Total: {self.calculate_hand()})"
    
  
  def __repr__(self):
    return self.__str__()
  
  
class Player(Person):
  def __init__(self, name, money = 50):
    super().__init__()
    self.name = name
    self.money = money
    self.bet = 0

  def equality(self):
    self.money+=self.bet
    self.bet=0
  
  def win(self):  
    self.bet=0
  
  def lose(self):
    self.bet=0
  
  def set_bet(self, new_bet):
    self.bet = new_bet
    self.money -= new_bet
  
  def __str__(self):
    return f"{self.name}: {self.hand} (Total: {self.calculate_hand()}) - Money: {self.money} - Bet: {self.bet}"
  
  def __repr__(self):
      return self.__str__()