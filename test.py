import re
from socket import *
from bs4 import BeautifulSoup
from lxml import objectify


def get_opstock(date_str):
	with open('OpStock.req', 'rb') as fp:
		data = fp.read()
	date = date_str.encode()
	pat = re.compile(b'\d{8}')
	data = pat.sub(date, data)

	cs = socket(AF_INET, SOCK_STREAM)
	cs.connect((host, port))
	cs.send(req)
	response = b''

	while True:
		response += cs.recv(1024)
		if response[-1] == 11:
			break
	return response



def opstock_contents_parser(contents):
	content_pat = re.compile(b'<NewDataSet>.+<\/NewDataSet>')
	content = content_pat.findall(contents)
	soup = BeautifulSoup(content[1], 'html.parser')
	ret = []
	# for table in soup.newdataset.find_all('table1'):

	# 	record = {
	# 		'약품코드': table.drug_cd.text if table.drug_cd else "",
	# 		'약품명' : table.drug_nm.text if table.drug_nm else "",
	# 		'규격단위' : table.stock_unit.text if table.stock_unit else "",
	# 		'재고' : table.stock_qty.text if table.stock_qty else ""
	# 	}
	# 	ret.append(record)
	# return ret
	for table in soup.find_all('table1'):
		ret.append({elm.name: elm.text for elm in table.children})
	return ret



with open('OpStock.sample', 'rb') as fp:
	response = fp.read()
	# print(response)
ret = opstock_contents_parser(response)


print(ret)
