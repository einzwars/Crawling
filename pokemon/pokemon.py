import logging
import os
import re
import sys
import traceback
from urllib.request import urlretrieve
import time

from PyQt5.QtCore import QThread
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#GUI
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QGridLayout, QProgressBar, QTextBrowser

#오류 추적
logging.basicConfig(level=logging.ERROR)

def web_connect():
    global driver
    #크롬 옵션
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    #크롬 드라이버
    # if  getattr(sys, 'frozen', False):
    #     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    #     driver = webdriver.Chrome('./chromedriver', options=options)
    # else:
    #     driver = webdriver.Chrome('./chromedriver', options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://pokemon.fandom.com/ko/wiki/%EC%9D%B4%EC%83%81%ED%95%B4%EC%94%A8_(%ED%8F%AC%EC%BC%93%EB%AA%AC)")
    driver.implicitly_wait(300)

class miningThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        mining()

class pokemon_gui(QWidget) :

    def __init__(self):
        super().__init__()
        self.threadclass = miningThread()
        self.start()
        self.log()
        self.initUI()

    def start(self):
        self.startBtn = QPushButton('시작', self)
        self.startBtn.resize(self.startBtn.sizeHint())
        self.startBtn.clicked.connect(self.action)

    def action(self):
        global stop
        stop = True
        self.threadclass.start()
        self.progress()

        if stop :
            self.startBtn.setText('중지')
            self.startBtn.clicked.connect(self.stopAction)
        else:
            self.startBtn.setText('실행')
            self.startBtn.clicked.connect(self.startAction)

    def startAction(self):
        stop = True

    def stopAction(self):
        stop = False

    def log(self):
        global label
        label = QTextBrowser()
        label.setStyleSheet(
            "border-style: solid;"
            "border-width: 2px;"
            "border-radius: 3px"
        )

    def progress(self):
        self.completed = 1
        while self.completed < 100:
            self.pbar.setProperty("value", self.completed)
            QApplication.processEvents()
            self.completed += 0.5
            time.sleep(0.5)
        QApplication.processEvents()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.pbar = QProgressBar(self)

        grid = QGridLayout()
        grid.addWidget(label, 0, 0)
        grid.addWidget(self.pbar, 1, 0)
        grid.addWidget(self.startBtn, 2, 0)
        self.setLayout(grid)

        self.setWindowTitle('포켓몬 데이터 수집기')
        self.setWindowIcon(QIcon('lizardon.png'))
        self.center()
        self.resize(480, 400)
        self.show()

#이미지, 텍스트 저장 폴더 생성
try:
    if not (os.path.isdir('./pokemon/pokemon_img')):
        os.makedirs(os.path.join('./pokemon/pokemon_img'))
except OSError as e:
    if e.errno != e.errno.EEXIST:
        print("폴더 생성 실패!")
        exit()


def mine():
    global stat, stat2, stat3, data, table, table2, table3, soup

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    data = soup.find('div', {'class':'infobox-pokemon'})
    table = driver.find_element_by_xpath('//*[@id="mw-content-text"]/table[3]/tbody').text
    stat = table.split('\n')
    table2 = driver.find_element_by_xpath('//*[@id="mw-content-text"]/table[4]/tbody').text
    stat2 = table2.split('\n')
    table3 = driver.find_element_by_xpath('//*[@id="mw-content-text"]/table[5]/tbody').text
    stat3 = table3.split('\n')


def stat_info():
    global pokemon_hp, pokemon_atk, pokemon_def, pokemon_satk, pokemon_sdef, pokemon_spd, pokemon_sum
    if len(table)>=250 :
        pokemon_hp = stat[2]
        pokemon_atk = stat[4]
        pokemon_def = stat[6]
        pokemon_satk = stat[8]
        pokemon_sdef = stat[10]
        pokemon_spd = stat[12]
        pokemon_sum = stat[14]
    elif len(table)<=250 and len(table2)>=250 :
        pokemon_hp = stat2[2]
        pokemon_atk = stat2[4]
        pokemon_def = stat2[6]
        pokemon_satk = stat2[8]
        pokemon_sdef = stat2[10]
        pokemon_spd = stat2[12]
        pokemon_sum = stat2[14]
    else :
        pokemon_hp = stat3[2]
        pokemon_atk = stat3[4]
        pokemon_def = stat3[6]
        pokemon_satk = stat3[8]
        pokemon_sdef = stat3[10]
        pokemon_spd = stat3[12]
        pokemon_sum = stat3[14]

    return pokemon_hp, pokemon_atk, pokemon_def, pokemon_satk, pokemon_sdef, pokemon_spd, pokemon_sum

def name():
    global pokemon_name
    pokemon_name = data.find('strong').text
    return pokemon_name

def num():
    global pokemon_num
    pokemon_num = data.find('strong', {'class':'rounded'}).text
    return pokemon_num

def type():
    global pokemon_type
    type_list = data.findAll('span', {'class':'split-cell'})
    if len(type_list)>=2:
        pokemon_type = type_list[0].text + ', ' + type_list[1].text
    else:
        pokemon_type = type_list[0].text
    return pokemon_type

def sort():
    global pokemon_sort
    pokemon_sort = re.sub('\n', '', data.find(text = re.compile("[ㄱ-힝]포켓몬")))
    return pokemon_sort

def ability():
    global pokemon_ability, pokemon_hidden
    ability_list = data.findAll('span', {'class':'ajaxttlink'})
    if len(ability_list)>=3:
        pokemon_ability = ability_list[0].text + ', ' + ability_list[1].text
        pokemon_hidden = ability_list[2].text
    elif len(ability_list)>=2:
        pokemon_ability = ability_list[0].text
        pokemon_hidden = ability_list[1].text
    else:
        pokemon_ability = ability_list[0].text
        pokemon_hidden = "없음"
    return pokemon_ability, pokemon_hidden

def size():
    global pokemon_height, pokemon_weight
    pokemon_height = re.sub('\n', '', data.find(text = re.compile("[0-9]m")))
    pokemon_weight = re.sub('\n', '', data.find(text = re.compile("[0-9]kg")))
    return pokemon_height, pokemon_weight

def gender():
    global pokemon_mgender, pokemon_fgender
    pokemon_mgender = re.sub('\n', '', data.findAll(text = re.compile("[0-9]%"))[0])
    pokemon_fgender = re.sub('\n', '', data.findAll(text = re.compile("[0-9]%"))[1])
    return pokemon_mgender, pokemon_fgender

def birth():
    global pokemon_birth
    pokemon_birth = re.sub('\n', '', data.find(text = re.compile("[0-9]걸음")))
    return pokemon_birth

#txt 저장
text = ''
def text_save():
    global text
    text = text + "이름 :" + pokemon_name +'\n'+ "번호 : " + pokemon_num +'\n'+  "타입 : " + pokemon_type +'\n'+ "분류 :"  + pokemon_sort +'\n'+ "특성 : " + pokemon_ability +'\n'+ "숨겨진 특성 : " + pokemon_hidden +'\n'+ "키 :" + pokemon_height +'\n'+ "몸무게 :" + pokemon_weight +'\n'+ \
           "성비 : 수컷-" + pokemon_mgender + " 암컷-" + pokemon_fgender +'\n'+ "부화 걸음 수 : " + pokemon_birth +'\n'+ "--------종족값--------" +'\n'+ pokemon_hp +'\n'+ pokemon_atk +'\n'+ pokemon_def +'\n'+ pokemon_satk +'\n'+ \
           pokemon_sdef +'\n'+ pokemon_spd +'\n'+ pokemon_sum +'\n'+'\n'
    open_output_text = open('./pokemon/pokemon.txt', 'w', encoding='utf-8')
    open_output_text.write(text)
    open_output_text.close()

#포켓몬 이미지 저장
def img_save():
    img = data.find('a', {'title':'이미지'})
    img_name = pokemon_name
    img_src = img['href']
    urlretrieve(img_src, './pokemon/pokemon_img/' + img_name + '.jpg')

def next():
    btn = driver.find_element_by_link_text('→')
    btn.click()

def mining():
    try:
        web_connect()
        while stop :
            mine()
            print("이름 :"+name())
            print("번호 : "+num())
            print("타입 : "+type())
            print("분류 :"+sort())
            print("특성 : "+ability()[0])
            print("숨겨진 특성 : "+ability()[1])
            print("키 :"+size()[0])
            print("몸무게 :"+size()[1])
            print("성비 : 수컷-"+gender()[0] + " 암컷-"+gender()[1])
            print("부화 걸음 수 : "+birth())
            print("--------종족값--------")
            print(stat_info()[0])
            print(stat_info()[1])
            print(stat_info()[2])
            print(stat_info()[3])
            print(stat_info()[4])
            print(stat_info()[5])
            print(stat_info()[6])
            print("")
            text_save()
            label.append(
                "이름 :" + pokemon_name +'\n'+ "번호 : " + pokemon_num +'\n'+  "타입 : " + pokemon_type +'\n'+ "분류 :"  + pokemon_sort +'\n'+ "특성 : " + pokemon_ability +'\n'+ "숨겨진 특성 : " + pokemon_hidden +'\n'+ "키 :" + pokemon_height +'\n'+ "몸무게 :" + pokemon_weight +'\n'+ \
                "성비 : 수컷-" + pokemon_mgender + " 암컷-" + pokemon_fgender +'\n'+ "부화 걸음 수 : " + pokemon_birth +'\n'+ "--------종족값--------" +'\n'+ pokemon_hp +'\n'+ pokemon_atk +'\n'+ pokemon_def +'\n'+ pokemon_satk +'\n'+ \
                pokemon_sdef +'\n'+ pokemon_spd +'\n'+ pokemon_sum +'\n'+'\n'
            )
            img_save()
            if(name() == ' 거북왕 ') :
                break
            QApplication.processEvents()
            time.sleep(3)
            next()
    except:
        logging.error(traceback.format_exc())

def main():
    try:
        app = QApplication(sys.argv)
        p = pokemon_gui()

    except Exception as e:
        logging.error(traceback.format_exc())
        # os.system("pause")

    finally:
        sys.exit(app.exec_())
        driver.close()

if __name__ == "__main__":
    main()