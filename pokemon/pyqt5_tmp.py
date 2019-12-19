import sys

from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QLabel, QGridLayout, QProgressBar


class pokemon_gui(QWidget) :

    def __init__(self):
        super().__init__()
        self.progress()
        self.time()
        self.control()
        self.log()
        self.initUI()

    # def close(self):
    #     self.closeBtn = QPushButton('닫기', self)
    #     self.closeBtn.resize(self.closeBtn.sizeHint())
    #     self.closeBtn.clicked.connect(QCoreApplication.instance().quit)
    #     self.closeBtn.setToolTip('닫기')

    def control(self):
        self.controlBtn = QPushButton('시작', self)
        self.controlBtn.resize(self.controlBtn.sizeHint())
        self.controlBtn.clicked.connect(self.doAction)
        self.controlBtn.setToolTip('시작')

    def time(self):
        self.timer = QBasicTimer()
        self.step = 0

    def log(self):
        self.label = QLabel('', self)
        self.label.setStyleSheet(
            "border-style: solid;"
            "border-width: 2px;"
            "border-radius: 3px"
        )

    def progress(self):
        self.pbar = QProgressBar(self)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.controlBtn.setText('완료')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.controlBtn.setText('계속')
        else:
            self.timer.start(100, self)
            self.controlBtn.setText('중지')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):

        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.pbar, 1, 0)
        grid.addWidget(self.controlBtn, 2, 0)
        self.setLayout(grid)

        self.setWindowTitle('포켓몬 데이터 수집기')
        self.setWindowIcon(QIcon('lizardon.png'))
        self.center()
        self.resize(480, 360)
        self.show()

app = QApplication(sys.argv)
p = pokemon_gui()
sys.exit(app.exec_())