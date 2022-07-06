from random import shuffle

class Card:

    faceCards = ["Jack", "King", "Queen"]
    card_fails = []

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

        if value in Card.faceCards:
            self.card_value = 10
        else:
            # Instantiating a Card with an 'Ace' raises ValueError
            try:
                self.card_value = int(value)
            except ValueError:
                self.card_value = None

    def __str__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    deck = []
    suits = ["Diamonds", "Hearts", "Spades", "Clovers"]
    values = ["2", "3", "4",
              "5", "6", "7",
              "8", "9", "10",
              "Ace", "Jack", "Queen", "King"]

    def __init__(self):
        for suit in Deck.suits:
            for value in Deck.values:
                self.deck.append(Card(suit, value))
        shuffle(self.deck)


    def remove_card(self):
        return self.deck.pop()


class Dealer:
    score = 0
    rounds_won = 0
    hand = []


    def __init__(self, name="Dealer"):
        self.name = name


    def recieve_card(self, card):
        """takes card objects as param"""
        self.hand.append(card)
        self.addScore_count(card)


    def addScore_count(self, card):
        if card.value == "Ace":
            if self.score <= 10:
                self.score += 11
            else:
                self.score += 1
        else:
            self.score += card.card_value


    def display_score(self):
        # score of the first card drawn
        first_card = self.hand[0]
        print(f"Dealer has a score of: {first_card.card_value}")


    # returns a boolean to see if dealer should deal another card
    def isDraw_card(self):
        if self.score <= 17:
            return True
        return False



class Player(Dealer):
    pass


class Game:
    # A perfect_hand is an automatic BlackJack, so must include all variations
    perfect_hand = [["Jack", "Ace"], ["King", "Ace"], ["Queen", "Ace"],
                    ["Ace", "Jack"], ["Ace", "King"], ["Ace", "Queen"]]

    def main(self):
        self.dealer = Dealer()
        self.player = Player("TestUser")
        self.deck = Deck()
        self.test_rounds = 4 # perform test rounds

        for i in range(self.test_rounds):
            print(f"The Deck has {len(self.deck.deck)}") # testing code
            self.restart_game()
            self.deal_cards(self.dealer)
            print("=" * 20, "\n") # for aesthetic displaying purpose
            self.deal_cards(self.player)
            print("=" * 20, "\n")
            bust = False
            player_blackjack = self.isBlackJack(self.player)
            dealer_blackjack = self.isBlackJack(self.dealer)

            if player_blackjack:
                print("BlackJack!\nCongratulations!!")
                print("=" * 20, "\n")
                self.display_finalScore()
                continue
            elif dealer_blackjack:
                print("Better luck next time!")
                print("=" * 20, "\n")
                self.display_finalScore()
                continue

            # Player loop
            while self.player.score <= 21:

                self.display_currentScore()

                print("'HIT' or 'STAY?'")
                response = input("").upper()

                if response == "HIT":

                    card = self.deck.remove_card()
                    self.player.recieve_card(card)

                    print(f"{self.player.name}" + " drew", card)

                    # if self.player.score > 21:
                    #     print("Busts\nBetter luck next time!")
                    #     print("=" * 20, "\n")
                    #     break
                    if self.player.score == 21:
                        player_win = True
                        break

                elif response == "STAY":
                    break

            # Dealer loop
            while self.dealer.score <= 17:
                print("Dealer's hand:")
                for card in self.dealer.hand:
                    print(card, end="|")
                card = self.deck.remove_card()
                self.dealer.recieve_card(card)

                print("dealer" + " drew", card, end="\n")
                if self.dealer.score == 21:
                    dealer_win = True

            # when player and dealer don't busts
            if self.player.score < 21 and self.dealer.score < 21:
                if self.player.score > self.dealer.score:
                    self.display_finalScore()
                    print("Congratulations\nYou win this round!")
                    print("=" * 20, "\n")
                # if player and dealer have same score: it's a lose
                else:
                    self.display_finalScore()
                    print("Better luck next time ")
                    print("=" * 20, "\n")
                    break

            # when player or dealer busts
            if self.player.score > 21 or self.dealer.score > 21:
                if self.player.score > 21:
                    self.display_finalScore()
                    print("Better luck next time ")
                    print("=" * 20, "\n")
                else:
                    self.display_finalScore()
                    print("Congratulations\nYou win this round!")
                    print("=" * 20, "\n")

            # when player or dealer hit blackjack
            elif player_win or dealer_win:
                if player_win:
                    self.display_finalScore()
                    print("Congratulations\nYou win this round!")
                    print("=" * 20, "\n")
                else:
                    self.display_finalScore()
                    print("dealer hits BlackJack!")
                    print("Better luck next time ")
                    print("=" * 20, "\n")




    # deals two cards to player and dealer
    def deal_cards(self, card_reciever): # buggy code
            for i in range(2):
                card = self.deck.remove_card()
                card_reciever.recieve_card(card)

                if card_reciever is self.player:
                    print(f"{self.player.name} drew {card}")
                # this is the dealer's starting hand: score is unknown
                elif card_reciever is self.dealer and len(self.dealer.hand) < 2:
                    print(f"Dealer drew {card_reciever.hand[0]}")


    def isBlackJack(self, player):
        """
        player perimeter is a player instance,
        compares the list of cards drawn to 'player' and return Boolean
        if dealt a perfect hand known as BlackJack
        """
        player_hand = [card.value for card in player.hand]

        if player_hand in self.perfect_hand:
            return True
        return False


    # called at the end of round,
    def isWinner(self):
        player_score = self.player.score
        dealer_score = self.dealer.score
        if player_score > dealer_score:
            return True
        return False


    def display_finalScore(self):
        print(f"{self.player.name} has a score of: {self.player.score}")
        print(f"{self.dealer.name} has a score of: {self.dealer.score}")


    def display_currentScore(self):
        print(f"{self.player.name} has a score of: {self.player.score}")
        self.dealer.display_score()


    # You have to restart the game after end result of comparison
    def restart_game(self):
        self.player.hand = []
        self.dealer.hand = []
        self.player.score = 0
        self.dealer.score = 0
        self.bust = False


if __name__ == "__main__":
    # try statement is for debugging purposes
    try:
        game = Game()
        game.main()
    except KeyboardInterrupt:
        exit()

# TODO: check for wins in all scenarios at end of while loops.
