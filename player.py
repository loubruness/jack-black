class Player:
  def __init__(self, name, money = 50):
    self.name = name
    self.money = money
    self.bet = 0
    self.hand = []

  def get_name(self):
    return self.name

  def get_money(self):
    return self.money

  def set_money(self, new_money):
    self.money = new_money
    
  def get_bet(self):
    return self.bet
  
  def set_bet(self, new_bet):
    self.bet = new_bet
    self.money -= new_bet
  
  def get_hand(self):
    return self.hand
  
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
    
  def __str__(self):
    return f"{self.get_name}: {self.get_hand} (Total: {self.calculate_hand}) - Money: {self.get_money}"
