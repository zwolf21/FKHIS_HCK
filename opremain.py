from socket import * 
import sys, os, re
from itertools import groupby
from operator import itemgetter
from io import BytesIO
from collections import OrderedDict

import xlrd
import xlsxwriter
from bs4 import BeautifulSoup

try:
	from .db import drugDB, reportElm
	from .settings import *
	from .recordlib import RecordParser
except:
	from db import drugDB, reportElm
	from settings import *
	from recordlib import RecordParser

host = SERVER
port = PORT


def opremain_query(start_date, end_date, qry_path):
	start_date = start_date.replace('-', '')
	end_date = end_date.replace('-', '')
	p = re.compile(b'\d{8}')
	content_pat = re.compile(b'<NewDataSet>.+<\/NewDataSet>')
	with open(qry_path, 'rb') as fp:
		req = fp.read()
		cs = socket(AF_INET, SOCK_STREAM)
		cs.settimeout(20)
		cs.connect((host, port))
		req = p.sub(start_date.encode(), req)
		req= p.sub(end_date.encode(), req, 1)
		cs.send(req)
		rsp = b''
		while True:
			rsp += cs.recv(1024)
			if rsp[-1] == 11:
				cs.close()
				break
		return  content_pat.findall(rsp)
		


def parse_narc_content(content, n=0):
	soup = BeautifulSoup(content, 'html.parser')
	recs = RecordParser(
		records = [OrderedDict((child.name, child.text) for child in table.children) for table in soup.find_all('table1')],
		drop_if = lambda row: not row.get('narct_owarh_ymd') or row['drug_cd']  not in drugDB
	)
	recs.select(['narct_owarh_ymd', 'ward', 'ori_ord_ymd', 'ord_no', 'ptnt_no', 'ptnt_nm', 'drug_cd', 'drug_nm', 'ord_qty_std', 'tot_qty'], 
		where = lambda row: row['ret_gb'] not in ['D/C', '반납']
	)
	recs.vlookup(drugDB.values(), 'drug_cd', 'code', [('amount', 0), ('amount_unit', ''), ('name', ""), ('std_unit', "")])
	recs.format([('tot_qty', 0.0), ('ord_qty_std', 0.0)])
	recs.add_column([('잔량', lambda row: row['tot_qty'] - row['ord_qty_std']), ('폐기량', lambda row: row['잔량'] * row['amount'])])
	recs.select('*', where= lambda row: row['잔량'] > 0).order_by(['name', 'narct_owarh_ymd', 'ward'])
	recs.rename([
		('narct_owarh_ymd', '불출일자'), ('ori_ord_ymd', '원처방일자'), ('ord_no', '처방번호[묶음]'), ('tot_qty', '집계량'), 
		('name', '폐기약품명'), ('drug_cd', '약품코드'), ('amount', '집계량'), ('ord_qty_std', '처방량(규격단위)'), ('drug_nm', '폐기약품명'), 
		('amount_unit', '폐기단위'), ('ptnt_nm', '환자명'), ('ptnt_no', '환자번호'), ('std_unit', '규격단위'), ('ward', '병동')
	])
	table = recs.select(['불출일자', '병동', '환자번호', '환자명', '폐기약품명','약품코드', '처방량(규격단위)', '잔량', '규격단위', '폐기량', '폐기단위' ]).to2darry()
	grp = recs.group_by(
			columns = ['폐기약품명'], 
			aggset=[('폐기량', sum, '폐기량__sum'), ('폐기약품명', len, '폐기약품명__len')], 
			selects = ['폐기약품명', '폐기약품명__len', '규격단위', '폐기량__sum', '폐기단위', '약품코드'],
			inplace=False
		)

	return table[n:], grp


	# -------------------------------------------------------------------------------------------------------------------------------------------------

def excel_output(exl_table, grp):

	date_index = set(row[0] for r, row in enumerate(exl_table) if r >0)
	first_date, last_date = min(date_index), max(date_index)
	title = '{}~{} 마약류 폐기 현황'.format(first_date, last_date)
	fname = '{}.xlsx'.format(title)
	select_columns = ['불출일자', '병동', '환자번호', '환자명', '폐기약품명', '약품코드', '처방량(규격단위)', '잔량', '규격단위', '폐기량', '폐기단위' ]

	output = BytesIO()
	wb = xlsxwriter.Workbook(output)
	ws = wb.add_worksheet()

	title_format = wb.add_format({'align': 'center', 'bold': True, 'font_size':20})
	float_format = wb.add_format({'num_format': '0.00'})
	ml_format = wb.add_format({'num_format': '0.00 "ml"'})
	mg_format = wb.add_format({'num_format': '0.00 "mg"'})
	g_format = wb.add_format({'num_format': '0.00 "g"'})

	formats = \
	{
		'title': title_format,
		'float': float_format,
		'ml': ml_format,
		'mg': mg_format,
		'g': g_format,
	}

	ws.merge_range(0,0,0, len(exl_table[0])-2, title, formats['title'])

	ws.set_column('A:A',9)	# 불출일자
	ws.set_column('B:B',3)	# 병동
	ws.set_column('C:C',10)	# 환자번호
	ws.set_column('D:D',6)	# 환자명
	ws.set_column('E:E',20)	# 폐기약품명
	ws.set_column('F:F',5)	# 처방량(규격단위)
	ws.set_column('G:G',5)	# 잔량
	ws.set_column('H:H',5)	# 규격단위
	ws.set_column('I:I',9)	# 폐기량

	for r, row in enumerate(exl_table):
		for c, data in enumerate(row):
			if select_columns[c] == '폐기단위':
				continue

			if select_columns[c] == '폐기량' and r >0:
				ws.write(r+1, c, data, formats[row[-1]])
			elif select_columns[c] == '처방량(규격단위)' and r > 0:
				ws.write(r+1, c, float(data), formats['float'])
			else:
				ws.write(r+1, c, data)

	appen_r = r + 3
	ws.write(appen_r, 3, '종합')
	ws.write(appen_r, 4, '폐기약품명')
	ws.write(appen_r, 5, '')
	ws.write(appen_r, 6, '수량')
	ws.write(appen_r, 7, '규격')
	ws.write(appen_r, 8, '폐기량')
	appen_r +=1
	
	for r, row in enumerate(grp):
		ws.write(appen_r+r, 4, row['폐기약품명'])
		ws.write(appen_r+r, 6, row['폐기약품명__len'])
		ws.write(appen_r+r, 7, row['규격단위'])
		ws.write(appen_r+r, 8, row['폐기량__sum'], formats[drugDB[row['약품코드']]['amount_unit']])



	ws2 = wb.add_worksheet('보고서')

	ws2.set_column('A:A',12)	# 제조자
	ws2.set_column('B:B',25)	# 약품명
	ws2.set_column('C:C',5)		# 구분
	ws2.set_column('D:D',20)	# 성분명
	ws2.set_column('E:E',5)		# 제형
	ws2.set_column('F:F',15)	# 제조번호
	ws2.set_column('G:G',12)	# 유효기한
	ws2.set_column('H:H',9)		# 폐기량
	ws2.set_column('I:I',5)		# 개수
	ws2.set_column('J:J',5)		# 규격



	y, m, d = last_date.split('-')
	title2 = '{}년 {}월 잔여마약류 폐기 결과보고'.format(y, m)

	cr = 0
	ws2.merge_range(cr, 0, cr, 9, title2, formats['title'])
	cr+=1

	fm1 = wb.add_format({'align': 'left', 'bold': True, 'font_size':15, 'border':True})
	ws2.merge_range(cr, 0, cr, 9, '보고인(공무원)', fm1)
	cr+=1

	fm2 = wb.add_format({'align': 'center', 'font_size': 12, 'bold': True, 'border':True})
	ws2.merge_range(cr,0,cr,1, '성명', fm2)
	ws2.merge_range(cr,2,cr,3, '생년월일', fm2)
	ws2.merge_range(cr,4,cr,5, '전화번호', fm2)
	ws2.merge_range(cr,6,cr,7, '등록번호', fm2)
	ws2.merge_range(cr,8,cr,9, '허가종별', fm2)
	cr+=1

	fm3 = wb.add_format({'align':'center', 'font_size': 12, 'border':True})
	ws2.merge_range(cr, 0, cr, 1, reportElm['repoter']['name'], fm3)
	ws2.merge_range(cr, 2, cr, 3, reportElm['repoter']['birth'], fm3)
	ws2.merge_range(cr, 4, cr, 5, reportElm['repoter']['tel'], fm3)
	ws2.merge_range(cr, 6, cr, 7, reportElm['repoter']['assign_num'], fm3)
	ws2.merge_range(cr, 8, cr, 9, reportElm['repoter']['perm_class'], fm3)
	cr +=1

	fm4 = wb.add_format({'align':'center', 'font_size': 15, 'valign':'vcenter', 'border':True})
	ws2.merge_range(cr, 0, cr+1, 1, '업소명칭', fm4)
	ws2.merge_range(cr, 2, cr+1, 3, '대표자', fm4)

	ws2.merge_range(cr, 4, cr, 9, '업소 소재지', fm3)
	cr+=1

	ws2.merge_range(cr, 4, cr, 5, '지역', fm3)
	ws2.merge_range(cr, 6, cr, 9, '세부주소', fm3)
	cr+=1

	fm5 = wb.add_format({'align':'center', 'font_size': 10, 'border':True})
	ws2.merge_range(cr, 0, cr, 1, reportElm['repoter']['market'], fm5)
	ws2.merge_range(cr, 2, cr, 3, reportElm['repoter']['name'], fm5)
	ws2.merge_range(cr, 4, cr, 5, reportElm['repoter']['region'], fm5)
	ws2.merge_range(cr, 6, cr, 9, reportElm['repoter']['address'], fm5)
	cr+=1

	ws2.merge_range(cr, 0, cr, 9, "")
	cr+=1

	ws2.merge_range(cr, 0, cr, 9, '폐기정보', fm1)
	cr+=1

	ws2.merge_range(cr, 0, cr, 1, '폐기일시', fm2)
	ws2.merge_range(cr, 2, cr, 9, reportElm['remainInfo']['date'], fm2)
	cr+=1

	ws2.merge_range(cr, 0, cr, 1, '입회자(부서 및 성명)', fm5)
	ws2.merge_range(cr, 2, cr, 3, '폐기자 (부서 및 성명)', fm5)
	ws2.merge_range(cr, 4, cr, 7, '폐기장소', fm5)
	ws2.merge_range(cr, 8, cr, 9, '폐기방법', fm5)
	cr+=1

	ws2.merge_range(cr, 0, cr, 1, reportElm['remainInfo']['observer'], fm5)
	ws2.merge_range(cr, 2, cr, 3, reportElm['remainInfo']['supervisor'], fm5)
	ws2.merge_range(cr, 4, cr, 7, reportElm['remainInfo']['place'], fm5)
	ws2.merge_range(cr, 8, cr, 9, reportElm['remainInfo']['method'], fm5)
	cr+=1

	ws2.merge_range(cr, 0, cr, 6, '사유', fm5)
	ws2.merge_range(cr, 7, cr, 9, '세부사유', fm5)
	cr+=1

	ws2.merge_range(cr, 0, cr, 6, reportElm['remainInfo']['reason'], fm5)
	ws2.merge_range(cr, 7, cr, 9, reportElm['remainInfo']['reasonDetail'], fm5)
	cr+=1

	ws2.merge_range(cr, 0, cr, 9, "")
	cr+=1

	ws2.merge_range(cr, 0, cr, 9, '폐기마약류', fm1)
	cr+=1

	fm7 = wb.add_format({'align':'center', 'border':True})
	ws2.write(cr, 0, '제조자(수입자)명', fm7)
	ws2.write(cr, 1, '약품명', fm7)
	ws2.write(cr, 2, '구분', fm7)
	ws2.write(cr, 3, '성분명', fm7)
	ws2.write(cr, 4, '제형', fm7)
	ws2.write(cr, 5, '제조번호', fm7)
	ws2.write(cr, 6, '유효기한', fm7)
	ws2.write(cr, 7, '폐기량', fm7)
	ws2.write(cr, 8, '개수', fm7)
	ws2.write(cr, 9, '규격', fm7)
	cr+=1


	fm6 = wb.add_format({'border':True})
	ml_format = wb.add_format({'num_format': '0.00 "ml"', 'border':True })
	mg_format = wb.add_format({'num_format': '0.00 "mg"', 'border':True })
	g_format = wb.add_format({'num_format': '0.00 "g"', 'border':True })

	formats = \
	{
		'title': title_format,
		'float': float_format,
		'ml': ml_format,
		'mg': mg_format,
		'g': g_format,
	}
	
	for r, row in enumerate(grp, cr):
		key = row['약품코드']
		firm = drugDB[key]['firm']
		name = drugDB[key]['name']
		cl = drugDB[key]['class']
		component = drugDB[key]['component']
		shape = drugDB[key]['shape']
		lot_num = " "
		expire = " "
		amount = row['폐기량__sum']
		fm_amount = formats[drugDB[key]['amount_unit']]
		count = row['폐기약품명__len']
		std_unit = drugDB[key]['std_unit']
		
		ws2.write(r, 0, firm, fm6)
		ws2.write(r, 1, name, fm6)
		ws2.write(r, 2, cl, fm6)
		ws2.write(r, 3, component, fm6)
		ws2.write(r, 4, shape, fm6)
		ws2.write(r, 5, lot_num, fm6)
		ws2.write(r, 6, expire, fm6)
		ws2.write(r, 7, amount, fm_amount)
		ws2.write(r, 8, count, fm6)
		ws2.write(r, 9, std_unit, fm6)

	wb.close()
	return output.getvalue()


def get_opremain_contents(start_date, end_date):

	
	xmls = opremain_query(start_date, end_date, os.path.join(BASE_DIR, 'requests/NarcOut.req'))
	xmls += opremain_query(start_date, end_date, os.path.join(BASE_DIR, 'requests/PsyOut.req'))

	table, grp = [], []
	for i, xml in enumerate(xmls):
		t, g = parse_narc_content(xml, 0 if i==0 else 1)
		table+=t
		grp+=g

	return excel_output(table, grp)



	# ret = parse_narc_content(content)
	# print(ret)




'''testcode'''
# with open(os.path.join(BASE_DIR, 'response_samples/OpRemain.sample.rsp'), 'rb') as fp:
# 	content = fp.read()

# tbl, grp = parse_narc_content(content)

# data = excel_output(tbl, grp)
# with open('test.xlsx', 'wb') as fp:
# 	fp.write(data)

# os.startfile('test.xlsx')
