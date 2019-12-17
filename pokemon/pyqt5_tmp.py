import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class pokemon_gui(QWidget) :

    def __init__(self):
        super().__init__()
        self.button()
        self.init()

    def button(self):
        btn = QPushButton('Button', self)
        btn.move(100, 100)
        btn.resize(btn.sizeHint())
        btn.setToolTip('버튼')

    def init(self):
        self.setWindowTitle('포켓몬 데이터 수집기')
        self.setWindowIcon(QIcon('lizardon.png'))
        self.setGeometry(2600, 300, 480, 360)
        self.show()

app = QApplication(sys.argv)
p = pokemon_gui()
sys.exit(app.exec_())