import random

class Card:
    def __init__(self, color, number=None, card_type=None):
        self.color = color
        self.number = number
        self.card_type = card_type

    def __str__(self):
        if self.card_type == 'wild':
            return 'Wild'
        elif self.card_type == 'wild4':
            return 'Wild Draw 4'
        elif self.number is not None:
            return f"{self.color} {self.number}"
        else:
            return f"{self.color} {self.card_type}"

class Deck:
    def __init__(self):
        self.cards = []
        for color in ['red', 'green', 'blue', 'yellow']:
            for i in range(10):
                self.cards.append(Card(color, number=i))
            self.cards.append(Card(color, card_type='skip'))
            self.cards.append(Card(color, card_type='reverse'))
            self.cards.append(Card(color, card_type='draw2'))
        for i in range(4):
            self.cards.append(Card(color=None, card_type='wild'))
            self.cards.append(Card(color=None, card_type='wild4'))
        random.shuffle(self.cards)
        self.discard_pile = []

    def draw_card(self):
        if len(self.cards) == 0:
            self.cards = self.discard_pile[:-1]
            random.shuffle(self.cards)
            self.discard_pile = [self.discard_pile[-1]]
        card = self.cards.pop()
        self.discard_pile.append(card)
        return card

    def discard(self, card):
        self.discard_pile.append(card)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)
        
class Game:
    def __init__(self, num_players):
        self.deck = Deck()
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]
        for i in range(7):
            for player in self.players:
                player.add_card(self.deck.draw_card())
        self.current_color = self.deck.discard_pile[-1].color
        self.current_player = 0
        self.direction = 1

    def choose_color(self, color):
        self.current_color = color

    def play_wild_card(self, card, color=None):
        self.players[self.current_player].remove_card(card)
        self.deck.discard(card)
        if len(self.players[self.current_player].hand) == 0:
            print(f"{self.players[self.current_player].name} wins!")
            return True
        elif card.card_type == 'wild':
            self.current_color = color
        elif card.card_type == 'wild4':
            next_player = (self.current_player + self.direction) % len(self.players)
            for i in range(4):
                self.players[next_player].add_card(self.deck.draw_card())
            self.current_color = color
        return False

    def run(self):
        # Draw the starting card from the deck
        self.deck.discard(self.deck.draw_card())

        # Loop through turns until a player wins
        while True:
            print(f"Current color: {self.current_color}")
            print(f"Current card: {self.deck.discard_pile[-1]}")
            print(f"Player {self.players[self.current_player].name}'s turn")

            player = self.players[self.current_player]

            # Check for UNO
            if len(player.hand) == 1:
                print(f"{player.name} has UNO!")

            # Display the player's hand
            print("Your hand:")
            for i, card in enumerate(player.hand):
                print(f"{i + 1}: {card}")

            # Get the player's choice of card
            choice = input("Enter the number of the card you want to play or 'd' to draw a card: ")
            if choice == 'd':
                player.add_card(self.deck.draw_card())
            else:
                try:
                    choice = int(choice)
                    card = player.hand[choice - 1]
                    if self.current_color is None or card.color == self.current_color or card.card_type == 'wild' or card.card_type == 'wild4':
                        if card.card_type == 'wild' or card.card_type == 'wild4':
                            color_choice = input("Choose a color (red, green, blue, yellow): ")
                            self.choose_color(color_choice)
                            if self.play_wild_card(card, color=color_choice):
                                return
                        else:
                            self.players[self.current_player].remove_card(card)
                            self.deck.discard(card)
                            if len(self.players[self.current_player].hand) == 0:
                                print(f"{self.players[self.current_player].name} wins!")
                                return
                            elif card.card_type == 'reverse':
                                self.direction *= -1
                            elif card.card_type == 'draw2':
                                next_player = (self.current_player + self.direction) % len(self.players)
                                for i in range(2):
                                    self.players[next_player].add_card(self.deck.draw_card())
                            elif card.card_type == 'skip':
                                next_player = (self.current_player + self.direction) % len(self.players)
                                self.current_player = (next_player + self.direction) % len(self.players)
                        if card.color is not None:
                            self.current_color = card.color
                            # Go to the next player
                            self.current_player = (self.current_player + self.direction) % len(self.players)
if __name__ == '__main__':
    num_players = int(input("Enter the number of players: "))
    game = Game(num_players)
    game.run()




