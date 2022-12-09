from PyQt5.QtWidgets import *
from view import *
import random

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.dealer_labels = (self.labeld1,self.labeld2,self.labeld3,self.labeld4,self.labeld5,self.labeld6,
                              self.labeld7,self.labeld8,self.labeld9,self.labeld10,self.labeld11,self.labeld12)
        self.player_labels = (self.labelp1,self.labelp2,self.labelp3,self.labelp4,self.labelp5,self.labelp6,
                              self.labelp7,self.labelp8,self.labelp9,self.labelp10,self.labelp11,self.labelp12)
        self.ace = {'Ace of Clubs', 'Ace of Diamonds', 'Ace of Spades', 'Ace of Hearts'}
        self.game_state = False
        self.clear_board()

        self.pushButtonPlay.clicked.connect(lambda: self.play())
        self.pushButtonQuit.clicked.connect(lambda: self.quit())
        self.pushButtonHit.clicked.connect(lambda: self.hit())
        self.pushButtonStand.clicked.connect(lambda: self.stand())

    def clear_board(self):
        for label in self.dealer_labels + self.player_labels:
            label.setVisible(False)
        self.dealer_hand = {}
        self.player_hand = {}
        self.dealer_sum = 0
        self.player_sum = 0
        self.dealer_label = 2
        self.player_label = 2
        self.dealer_hidden = None
        self.cards = {
            'Ace of Clubs': {'value': 11, 'path': 'cards/clubA.png'},'Ace of Diamonds': {'value': 11, 'path': 'cards/diamondA.png'},
            'Ace of Spades': {'value': 11, 'path': 'cards/spadeA.png'},'Ace of Hearts': {'value': 11, 'path': 'cards/heartA.png'},
            '2 of Clubs': {'value': 2, 'path': 'cards/club2.png'},'2 of Diamonds': {'value': 2, 'path': 'cards/diamond2.png'},
            '2 of Spades': {'value': 2, 'path': 'cards/spade2.png'},'2 of Hearts': {'value': 2, 'path': 'cards/heart2.png'},
            '3 of Clubs': {'value': 3, 'path': 'cards/club3.png'},'3 of Diamonds': {'value': 3, 'path': 'cards/diamond3.png'},
            '3 of Spades': {'value': 3, 'path': 'cards/spade3.png'},'3 of Hearts': {'value': 3, 'path': 'cards/heart3.png'},
            '4 of Clubs': {'value': 4, 'path': 'cards/club4.png'},'4 of Diamonds': {'value': 4, 'path': 'cards/diamond4.png'},
            '4 of Spades': {'value': 4, 'path': 'cards/spade4.png'},'4 of Hearts': {'value': 4, 'path': 'cards/heart4.png'},
            '5 of Clubs': {'value': 5, 'path': 'cards/club5.png'},'5 of Diamonds': {'value': 5, 'path': 'cards/diamond5.png'},
            '5 of Spades': {'value': 5, 'path': 'cards/spade5.png'},'5 of Hearts': {'value': 5, 'path': 'cards/heart5.png'},
            '6 of Clubs': {'value': 6, 'path': 'cards/club6.png'},'6 of Diamonds': {'value': 6, 'path': 'cards/diamond6.png'},
            '6 of Spades': {'value': 6, 'path': 'cards/spade6.png'},'6 of Hearts': {'value': 6, 'path': 'cards/heart6.png'},
            '7 of Clubs': {'value': 7, 'path': 'cards/club7.png'},'7 of Diamonds': {'value': 7, 'path': 'cards/diamond7.png'},
            '7 of Spades': {'value': 7, 'path': 'cards/spade7.png'},'7 of Hearts': {'value': 7, 'path': 'cards/heart7.png'},
            '8 of Clubs': {'value': 8, 'path': 'cards/club8.png'},'8 of Diamonds': {'value': 8, 'path': 'cards/diamond8.png'},
            '8 of Spades': {'value': 8, 'path': 'cards/spade8.png'},'8 of Hearts': {'value': 8, 'path': 'cards/heart8.png'},
            '9 of Clubs': {'value': 9, 'path': 'cards/club9.png'},'9 of Diamonds': {'value': 9, 'path': 'cards/diamond9.png'},
            '9 of Spades': {'value': 9, 'path': 'cards/spade9.png'},'9 of Hearts': {'value': 9, 'path': 'cards/heart9.png'},
            '10 of Clubs': {'value': 10, 'path': 'cards/club10.png'},'10 of Diamonds': {'value': 10, 'path': 'cards/diamond10.png'},
            '10 of Spades': {'value': 10, 'path': 'cards/spade10.png'},'10 of Hearts': {'value': 10, 'path': 'cards/heart10.png'},
            'Jack of Clubs': {'value': 10, 'path': 'cards/clubJ.png'},'Jack of Diamonds': {'value': 10, 'path': 'cards/diamondJ.png'},
            'Jack of Spades': {'value': 10, 'path': 'cards/spadeJ.png'},'Jack of Hearts': {'value': 10, 'path': 'cards/heartJ.png'},
            'Queen of Clubs': {'value': 10, 'path': 'cards/clubQ.png'},'Queen of Diamonds': {'value': 10, 'path': 'cards/diamondQ.png'},
            'Queen of Spades': {'value': 10, 'path': 'cards/spadeQ.png'},'Queen of Hearts': {'value': 10, 'path': 'cards/heartQ.png'},
            'King of Clubs': {'value': 10, 'path': 'cards/clubK.png'},'King of Diamonds': {'value': 10, 'path': 'cards/diamondK.png'},
            'King of Spades': {'value': 10, 'path': 'cards/spadeK.png'},'King of Hearts': {'value': 10, 'path': 'cards/heartK.png'}
        }

    def check_sum(self, hand, total_sum=0):
        for dict in list(hand.values()):
            total_sum += dict['value']
        return total_sum

    def check_status(self, decision):
        if self.player_sum > 21:
            self.label.setText(f'Your card value is {self.player_sum}, '
                               f'which is over 21. You lose. Retry? ')
            self.dealer_draw()
            self.game_state = False
            self.pushButtonPlay.setText('Play')
        elif self.player_sum <= 21:
            if self.player_sum == 21:
                decision = 'stand'
            if decision == 'hit':
                self.label.setText(f'Your card value is {self.player_sum}, '
                                   f'Would you like to hit or stand?')
            elif decision == 'stand':
                self.dealer_draw()
                self.game_state = False
                self.pushButtonPlay.setText('Play')
                if self.dealer_sum < self.player_sum or self.dealer_sum > 21:
                    self.label.setText(f'Your card value is {self.player_sum}, '
                                       f'The dealer card value is {self.dealer_sum}, '
                                       f'You won.')
                elif self.dealer_sum == self.player_sum:
                    self.label.setText(f'Your card value is {self.player_sum}, '
                                       f'The dealer card value is {self.dealer_sum}, '
                                       f'Uou tied.')
                elif self.dealer_sum > self.player_sum:
                    self.label.setText(f'Your card value is {self.player_sum}, '
                                       f'The dealer card value is {self.dealer_sum}, '
                                       f'You lost.')

    def play(self):
        self.game_state = True
        self.pushButtonPlay.setText('Forfeit')
        self.clear_board()
        for i in range(4):
            random_card = random.choice(list(self.cards.keys()))
            if i % 2 == 0:
                self.player_hand[random_card] = self.cards[random_card]
                del self.cards[random_card]
                self.player_labels[i//2].setPixmap(QtGui.QPixmap(self.player_hand[random_card]['path']))
                self.player_labels[i//2].setVisible(True)
                self.player_sum = self.check_sum(self.player_hand)
            elif i % 2 == 1:
                self.dealer_hand[random_card] = self.cards[random_card]
                del self.cards[random_card]
                self.dealer_labels[i//2].setPixmap(QtGui.QPixmap(self.dealer_hand[random_card]['path']))
                if i // 2 == 1:
                    self.dealer_hidden = random_card
                    self.dealer_labels[i // 2].setPixmap(QtGui.QPixmap('cards/empty.png'))
                self.dealer_labels[i//2].setVisible(True)
                self.dealer_sum = self.check_sum(self.dealer_hand)
        self.check_status('hit')

    def hit(self):
        if self.game_state == True:
            random_card = random.choice(list(self.cards.keys()))
            self.player_hand[random_card] = self.cards[random_card]
            del self.cards[random_card]
            self.player_labels[self.player_label].setPixmap(QtGui.QPixmap(self.player_hand[random_card]['path']))
            self.player_labels[self.player_label].setVisible(True)
            self.player_sum = self.check_sum(self.player_hand)
            if len(list(self.ace & set(self.player_hand.keys()))) > 0 and self.player_sum > 21:
                for key in list(self.ace & set(self.player_hand.keys())):
                    self.player_hand[key]['value'] = 1
                self.player_sum = self.check_sum(self.player_hand)
            self.player_label += 1
            self.check_status('hit')

    def dealer_draw(self):
        while self.dealer_sum < 17:
            random_card = random.choice(list(self.cards.keys()))
            self.dealer_hand[random_card] = self.cards[random_card]
            del self.cards[random_card]
            self.dealer_labels[self.dealer_label].setPixmap(QtGui.QPixmap(self.dealer_hand[random_card]['path']))
            self.dealer_labels[self.dealer_label].setVisible(True)
            self.dealer_sum = self.check_sum(self.dealer_hand)
            if len(list(self.ace & set(self.dealer_hand.keys()))) > 0 and self.dealer_sum > 21:
                for key in list(self.ace & set(self.dealer_hand.keys())):
                    self.dealer_hand[key]['value'] = 1
                self.dealer_sum = self.check_sum(self.dealer_hand)
            self.dealer_label += 1
        self.dealer_labels[1].setPixmap(QtGui.QPixmap(self.dealer_hand[self.dealer_hidden]['path']))

    def stand(self):
        if self.game_state == True:
            self.check_status('stand')

    def quit(self):
        exit()