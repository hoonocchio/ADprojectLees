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
		else:
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

			except:
				self.w_data = [{'a':'a'}]

	def resultList(self):
		resultList = []
		for w in self.w_data:
			if 'economyCharge' in w.keys() :
				resultList.append([w['depPlandTime'], w['airlineNm'], w['economyCharge']])

		return resultList
