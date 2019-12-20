#GUI 구현
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import datetime

from schedule import Schedule
#from weather import Weather
from dicts import airportdic, airlinedic


class Calendar(QWidget):

	def __init__(self):
		super().__init__()

		self.setWindowTitle('종강하고 여행가자!')
		self.resize(700, 700)
		self.sortKey = 'Low Price'

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

		self.cal = QCalendarWidget()
		self.cal.setVerticalHeaderFormat(0)
		self.cal.setDateRange(QDate.currentDate(), self.cal.maximumDate())
		# 날씨 정보 출력
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
		#grid.setColumnStretch(4,1)
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
		 #버튼 누를때마다 추가되는거 수정? 걍 냅둬?
		depairport = str(self.dep_combo.currentText())
		arrairport = str(self.arr_combo.currentText())
		depdate = self.forcolorList[0]
		airline = str(self.airline_com.currentText())

		self.schedule = Schedule(depairport, arrairport, depdate, airline)

		self.resultList1 = self.schedule.resultList()

		for i in self.resultList1:
			i[0] = i[0][:4] + "년" + i[0][4:6] + "월" + i[0][6:8] + "일" + i[0][8:10] + "시" + i[0][10:12] + "분"
			i[2] += "원"

		if len(self.forcolorList) > 1:
			depdate = self.forcolorList[-1]
			self.schedule = Schedule(arrairport, depairport, depdate, airline)
			self.resultList2 = self.schedule.resultList()
			for i in self.resultList2:
				i[0] = i[0][:4] + "년" + i[0][4:6] + "월" + i[0][6:8] + "일" + i[0][8:10] + "시" + i[0][10:12] + "분"
				i[2] += "원"

		inDex = QLabel('날짜'+'\t'*3+'  항공사'+'\t'*2+'가격')
		self.resultEdit = QTextEdit()
		sort = QPushButton("Sort")
		self.key_combo = QComboBox()

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

		if len(self.forcolorList) > 1:
			for x in self.forcolorList:
				date = QDate.fromString(x, "yyyyMMdd")
				self.cal.setDateTextFormat(date, fm)
			self.forcolorList.clear()

		fm2 = QTextCharFormat()
		fm2.setBackground(Qt.yellow)

		selecteddate = self.cal.selectedDate() #현재 선택한 날짜
		self.forcolorList.append(selecteddate.toString("yyyyMMdd"))

		if len(self.forcolorList) == 2:
			key = int(self.forcolorList[1]) - int(self.forcolorList[0])
			if key > 1:
				for i in range(1, key):
					self.forcolorList.append(str(int(self.forcolorList[0]) + i))
			elif key < 1:
				del self.forcolorList[0]

			self.forcolorList.sort()
			for x in self.forcolorList:
				date = QDate.fromString(x, "yyyyMMdd")
				self.cal.setDateTextFormat(date, fm2)


	def sortClicked(self):
		sortKey = self.key_combo.currentText()

		if sortKey == 'Low Price':
			self.resultList1 = sorted(self.resultList1, key=lambda result: result[2])
			if len(self.forcolorList) > 1:
				self.resultList2 = sorted(self.resultList2, key=lambda result: result[2])
		elif sortKey == 'Time':
			self.resultList1 = sorted(self.resultList1, key=lambda result: result[0])
			if len(self.forcolorList) > 1:
				self.resultList2 = sorted(self.resultList2, key=lambda result: result[0])
		else:
			self.resultList1 = sorted(self.resultList1, key=lambda result: result[1])
			if len(self.forcolorList) > 1:
				self.resultList2 = sorted(self.resultList2, key=lambda result: result[1])


		self.print()

	def print(self):
		result = ""

		for p in self.resultList1:
			result += str(p).replace('\'','').replace('[', '').replace(']', '').replace(',', '   ') + "\n"
		result += "\n"
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
