import urllib.request as ul
import xmltodict
import json
import sys
import io

from dicts import airportdic, airlinedic

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class Schedule:
	def __init__(self, depairport, arrairport, depdate, airline):
		self.depAirportId = airportdic[depairport]
		self.arrAirportId = airportdic[arrairport]

		if airline in airlinedic.keys():
			self.airlineId = airlinedic[airline]
		else: #선호하는 항공사가 없는 경우
			self.airlineId = None

		serviceKey = "hT4oaiwQY9nS2NWNXwjSI0MOVJG5%2B%2BZsEWy2QCkO%2FKCeZOJUJH37MmC0%2BrRZBz3yERyY1gZxXvdBOviPC0uRsg%3D%3D"


		url = "http://openapi.tago.go.kr/openapi/service/DmstcFlightNvgInfoService/getFlightOpratInfoList?serviceKey=" + serviceKey + "&numOfRows=70&pageNo=1&depAirportId=" + self.depAirportId + "&arrAirportId=" + self.arrAirportId + "&depPlandTime=" + depdate

		if self.airlineId != None:
			url += "&airlineId=" + self.airlineId

		request = ul.Request(url)
		response = ul.urlopen(request)
		rescode = response.getcode()

		if(rescode == 200):
			responseData = response.read()

			rD = xmltodict.parse(responseData)
			rDJ = json.dumps(rD)
			rDD = json.loads(rDJ)

			try:
				self.w_data = rDD["response"]["body"]["items"]["item"]

				if isinstance(self.w_data, list): #데이터가 한가지만 추출될 경우, 하나의 사전만 self.w_data에 저장되기 때문에 아래 w.keys()에서 오류가 발생한다.
					pass
				else:
					m = []
					m.append(self.w_data)
					self.w_data = m


			except:
				self.w_data = [{'a':'a', 'b':'b'}] #존재하는 항공편이 없는 경우 에는 item이 존재하지 않아 따로 처리 해주어야 함

	def resultList(self):
		resultList = []

		for w in self.w_data:
			if 'economyCharge' in w.keys() : # 항공권 가격이 없는 경우에 출력해주지 않기 위한 조건문
				resultList.append([w['depPlandTime'], w['airlineNm'], w['economyCharge']]) #리스트에 저장해서 반환. 튜플을 사용하면 출력창에서 출력될 데이터 수정을 하지 못함.

		return resultList
