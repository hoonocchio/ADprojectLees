#GUI 구현
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime
]
from schedule import Schedule
from dicts import airportdic, airlinedic


class Calendar(QWidget):

	def __init__(self):
		super().__init__()

		self.setWindowTitle('종강하고 여행가자!')
		self.resize(700, 700)
		self.sortKey = 'Low Price'

		#GUI 구성 시작
		depLabel = QLabel('출발 : ')
		self.dep_combo = QComboBox()
		arrLabel = QLabel('도착 : ')
		self.arr_combo = QComboBox()

		for ap in airportdic.keys():
			self.dep_combo.addItem(ap)
			self.arr_combo.addItem(ap)

		#콤보박스 초기값 설정
		self.dep_combo.setCurrentText("김포")
		self.arr_combo.setCurrentText("제주")

		#달력위젯
		self.cal = QCalendarWidget()
		self.cal.setVerticalHeaderFormat(0)
		self.cal.setDateRange(QDate.currentDate(), self.cal.maximumDate())

		self.finalButton = QToolButton()

		self.airline_com = QComboBox()

		self.airline_com.addItem("--선호하시는 항공사가 있으신가요?--")
		self.airline_com.addItem("없음")
		for al in airlinedic.keys():
			self.airline_com.addItem(al)


		self.finalButton.setText('Done')
		self.finalButton.clicked.connect(self.buttonClicked)
		self.forcolorList = []

		self.cal.clicked.connect(self.calendarClicked)

		grid = QGridLayout()
		grid.addWidget(depLabel,0,0)
		grid.addWidget(self.dep_combo,0,1,1,2)

		grid.addWidget(arrLabel,0,3)
		grid.addWidget(self.arr_combo,0,4,1,2)

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.airline_com)
		hbox.addWidget(self.finalButton)

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(grid)
		self.vbox.addWidget(self.cal)
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)

	def buttonClicked(self):

		depairport = str(self.dep_combo.currentText())
		arrairport = str(self.arr_combo.currentText())
		depdate = self.forcolorList[0]
		airline = str(self.airline_com.currentText())

		self.schedule = Schedule(depairport, arrairport, depdate, airline)

		self.resultList1 = self.schedule.resultList()

		for i in self.resultList1: #날짜에 년월일시간과 가격에 원을 붙여주기 위함.
			i[0] = i[0][:4] + "년" + i[0][4:6] + "월" + i[0][6:8] + "일" + i[0][8:10] + "시" + i[0][10:12] + "분"
			i[2] += "원"

		if len(self.forcolorList) > 1: #왕복으로 선택했을 경우에 돌아오는 항공권.
			depdate = self.forcolorList[-1]
			self.schedule = Schedule(arrairport, depairport, depdate, airline)
			self.resultList2 = self.schedule.resultList()
			for i in self.resultList2:
				i[0] = i[0][:4] + "년" + i[0][4:6] + "월" + i[0][6:8] + "일" + i[0][8:10] + "시" + i[0][10:12] + "분"
				i[2] += "원"

		inDex = QLabel('날짜'+'\t'*3+'  항공사'+'\t'*2+'가격')# Done버튼 눌렀을 때 출력창 추가
		self.resultEdit = QTextEdit()
		sort = QPushButton("Sort")
		self.key_combo = QComboBox()

		self.resultEdit.setReadOnly(True) #읽기모드

		self.key_combo.addItem("Low Price")
		self.key_combo.addItem("Time")
		self.key_combo.addItem("Airline")

		self.print()
		sort.clicked.connect(self.sortClicked)


		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.key_combo)
		hbox.addWidget(sort)

		self.vbox.addWidget(inDex)
		self.vbox.addWidget(self.resultEdit)
		self.vbox.addLayout(hbox)
		self.setLayout(self.vbox)

	def calendarClicked(self):

		fm = QTextCharFormat()
		fm.setBackground(Qt.white)

		if len(self.forcolorList) > 1: #새로운 날짜를 선택하고 싶을 때 색을 화이트로 초기화하고 리스트안에 있는 날짜들을 삭제
			for x in self.forcolorList:
				date = QDate.fromString(x, "yyyyMMdd")
				self.cal.setDateTextFormat(date, fm)
			self.forcolorList.clear()

		fm2 = QTextCharFormat()
		fm2.setBackground(Qt.yellow)

		selecteddate = self.cal.selectedDate() #현재 선택한 날짜
		self.forcolorList.append(selecteddate.toString("yyyyMMdd"))# QDate형식으로 되어있는 날짜를 문자열로 변환해주어 리스트에 저장

		if len(self.forcolorList) == 2: # 날짜를 두 개 선택했을 경우
			key = int(self.forcolorList[1]) - int(self.forcolorList[0])
			if key > 1: #왕복을 의도하고 날짜를 선택했을 때
				for i in range(1, key):
					self.forcolorList.append(str(int(self.forcolorList[0]) + i))
			elif key < 1: #날짜를 잘못 선택하여 다시 선택하고 싶을 때 (뒷 날짜를 선택하고 앞 날짜를 선택했을 경우이다.)
				del self.forcolorList[0]

			self.forcolorList.sort()
			for x in self.forcolorList:
				date = QDate.fromString(x, "yyyyMMdd")
				self.cal.setDateTextFormat(date, fm2)


	def sortClicked(self):
		sortKey = self.key_combo.currentText()

		sortdict = {'Low Price':'2', 'Airline':'1', 'Time':'0'} # 반복되는 구문을 수정하기 위해 사전을 이용함.

		for sd in sortdict.keys():
			if sortKey == sd:
				self.resultList1 = sorted(self.resultList1, key=lambda result: result[sortdict[sd]])
				if len(self.forcolorList) > 1: #왕복일 경우에 sorted해줌
					self.resultList2 = sorted(self.resultList2, key=lambda result: result[sortdict[sd]])

		self.print()

	def print(self):
		result = ""

		if len(self.resultList1) == 0: #항공권이 없을때 없음을 나타내 주는 기능
			if len(self.forcolorList) > 1:
				if len(self.resultList2) == 0:
					result = "해당하는 항공권이 없습니다."
			else:
				result = "해당하는 항공권이 없습니다."

		else:
			for p in self.resultList1:
				result += str(p).replace('\'','').replace('[', '').replace(']', '').replace(',', '   ') + "\n"

			result += "\n" #왕복일 때 항공권 구분을 위한 공백 처리 

			if len(self.forcolorList) > 1:
				for p in self.resultList2:
					result += str(p).replace('\'','').replace('[', '').replace(']', '').replace(',', '   ') + "\n"
			
		self.resultEdit.setText(result)



if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	airplane = Calendar()
	airplane.show()
	sys.exit(app.exec_())
