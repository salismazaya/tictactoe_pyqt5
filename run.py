import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from module import Tictactoe

app = QApplication(sys.argv)

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tictactoe")
        self.resize(288,512)
        self.turn_ = False
        self.p1_first = True
        self.p1_score = 0
        self.p2_score = 0
        self.aktif_ = [True] * 10
        self.image()

        self.gas = Tictactoe()
        info = QLabel("<h1>Tictactoe</h1>")
        info.setAlignment(Qt.AlignCenter)
        author = QLabel("Made with love by: SalisM3")
        author.setAlignment(Qt.AlignCenter)
        self.winner_ = QLabel()
        self.winner_.setText("<h3>Player 1 Turn" if self.p1_first else "<h3>Player 2 Turn")
        self.winner_.setAlignment(Qt.AlignCenter)

        self.restart_ = QPushButton("Play Again")
        self.restart_.setEnabled(False)
        self.restart_.clicked.connect(self.game_lagi)
        self.score_ = QLabel(f"{self.p1_score} : {self.p2_score}")
        self.score_.setAlignment(Qt.AlignCenter)

        daftarAngka = QGridLayout()
        grid = QVBoxLayout()
        grid.addWidget(QLabel())
        grid.addWidget(info)
        grid.addWidget(author)
        grid.addWidget(self.winner_)
        grid.addWidget(QLabel())
        self.tombol = [None] * 9
        for x in range(9):
            self.tombol[x] = QPushButton()
            self.tombol[x].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tombol[0].clicked.connect(lambda: self.terklik(1))
        self.tombol[1].clicked.connect(lambda: self.terklik(2))
        self.tombol[2].clicked.connect(lambda: self.terklik(3))
        self.tombol[3].clicked.connect(lambda: self.terklik(4))
        self.tombol[4].clicked.connect(lambda: self.terklik(5))
        self.tombol[5].clicked.connect(lambda: self.terklik(6))
        self.tombol[6].clicked.connect(lambda: self.terklik(7))
        self.tombol[7].clicked.connect(lambda: self.terklik(8))
        self.tombol[8].clicked.connect(lambda: self.terklik(9))


        daftarAngka.addWidget(self.tombol[0], 0, 0)
        daftarAngka.addWidget(self.tombol[1], 0, 1)
        daftarAngka.addWidget(self.tombol[2], 0, 2)
        daftarAngka.addWidget(self.tombol[3], 1, 0)
        daftarAngka.addWidget(self.tombol[4], 1, 1)
        daftarAngka.addWidget(self.tombol[5], 1, 2)
        daftarAngka.addWidget(self.tombol[6], 2, 0)
        daftarAngka.addWidget(self.tombol[7], 2, 1)
        daftarAngka.addWidget(self.tombol[8], 2, 2)

        grid.addLayout(daftarAngka)
        grid.addWidget(QLabel())
        grid.addWidget(self.score_)
        grid.addWidget(QLabel())
        grid.addWidget(self.restart_)
        grid.addWidget(QLabel())
        grid.addWidget(QLabel())
        self.setLayout(grid)

    def update_score(self):
        self.score_.setText(f"{self.p1_score} : {self.p2_score}")

    def game_lagi(self):
        self.turn_ = 0
        self.winner_.setText("")
        for x in range(9):
            self.tombol[x].setIcon(QIcon())
        self.restart_.setEnabled(False)
        self.aktif_ = [True] * 10

        self.p1_first = not self.p1_first
        self.winner_.setText("<h3>Player 1 Turn" if self.p1_first else "<h3>Player 2 Turn")

        self.image()
        
        self.coloumsControl()
        self.gas = Tictactoe()

    def coloumsControl(self, disable = False):
        for x in range(9):
            self.tombol[x].setEnabled(False if disable else True)

    def selected_(self, number):
        self.aktif_[number] = False

    def terklik(self, number):
        if self.aktif_[number]:
            self.turn_ = not self.turn_
            self.selected_(number)
            self.terklik_proses(number)

    def detect_winner(self):
        winner = self.gas.who_win()
        if winner in ["Player 1", "Player 2", "Draw"]:
            self.coloumsControl(disable = True)
            if not self.p1_first:
                winner = "Player 2" if winner == "Player 1" else "Player 1"
            self.winner_.setText("<h3>Winner: " + winner)
            self.restart_.setEnabled(True)
            return winner

    def image(self):
        if self.p1_first:
            self.t1_image = "img/bulet.png"
            self.t2_image = "img/silang.png"
        else:
            self.t2_image = "img/bulet.png"
            self.t1_image = "img/silang.png"

    def terklik_proses(self, number):
        if self.detect_winner() != "Draw":
            if self.turn_:
                self.tombol[number - 1].setIcon(QIcon(self.t1_image))
                self.gas.p1_select(number)
            else:
                self.tombol[number - 1].setIcon(QIcon(self.t2_image))
                self.gas.p2_select(number)
                # self.winner_.setText("<h3>Player 1 Turn")
            self.winner_.setText("<h3>Player 2 Turn" if not "2" in self.winner_.text() else "<h3>Player 1 Turn")
            winner = self.detect_winner()
            if winner in ["Player 1", "Player 2"]:
                if winner == "Player 1":
                    self.p1_score += 1
                else:
                    self.p2_score += 1
                self.update_score()

    # def terklik_proses2(self):
    #         p2_move = self.gas.computer_move()
    #         self.selected_(p2_move)
    #         self.tombol[p2_move - 1].setIcon(QIcon("img/silang.png"))
    #         self.gas.p2_select(p2_move)

    #         winner_ = self.gas.who_win()
    #         if winner_ in ["You", "Computer"]:

    #             if winner_ == "You":
    #                 self.p1_score += 1
    #             else:
    #                 self.p2_score += 1  

    #             self.winner_.setText("<h3>Winner: " + winner_)
    #             self.update_score()
    #             self.coloumsControl(disable = True)
    #             self.restart_.setEnabled(True)

main = Main()
main.show()

app.exec_()