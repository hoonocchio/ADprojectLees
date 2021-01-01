import unittest

from schedule import Schedule

class Test(unittest.TestCase):

	def setUp(self):
		self.s1 = Schedule("NAARKTH","NAARKSI","20200120","")
		self.s2 = Schedule("NAARKSS","NAARKNY","20191225","")

	def tearDown(self):
		pass

	def testSchedule(self):
		self.assertEqual(isinstance(self.s1.w_data, list), True)
		#데이터가 한가지만 추출될 경우, 하나의 사전만 self.w_data에 저장되기 때문에 아래 w.keys()에서 오류가 발생한다. list로 잘 변환되는지 확인하는 testcase
		self.assertEqual(self.s1.resultList(), [])
		#데이터에 가격이 포함되어있지 않아 결과값에는 아무것도 추가되지 않아야 한다
		self.assertEqual(self.s2.w_data, [{'a':'a', 'b':'b'}])
		#데이터에 아무것도 저장되어 있지 않은 경우에 [{'a':'a', 'b':'b'}]이 데이터리스트에 들어가는지 확인
		self.assertEqual(self.s2.resultList(), [])
