from itertools import groupby
from operator import itemgetter
import xlrd
import xlsxwriter

class ExcelParser:

	def __init__(self, xl_path = None, file_content=None, sheet_index=0, records=None, **extra_fields):
		if not records:
			wb = xlrd.open_workbook(xl_path) if xl_path else xlrd.open_workbook(file_contents=file_content)
			ws = wb.sheet_by_index(sheet_index)
			fields = ws.row_values(0)
			self._records = [dict(zip(fields, ws.row_values(i))) for i in range(1, ws.nrows)]
		else:
			self._records = records

		for row in self._records:
			row.update(**extra_fields)

	def __getitem__(self, index):
		return self._records[index]
	
	def __len__(self):
		return len(self._records)

	def __call__(self):
		return self._records

	def select(self, *fields, where=lambda row:row, as_table=False):
		if not fields:
			fields = self._records[0].keys()	
		ret =  [{k:v for k, v in row.items() if k in fields} for row in self._records if where(row)]
		self._records = ret
		if as_table:
			return [list(fields)] + [[row[col] for col in fields] for row in self._records]
		return self

	def order_by(self, *rules):
		for rule in reversed(rules):
			rvs = rule.startswith('-')
			rule = rule.strip('-')
			self._records.sort(key=lambda x: x[rule], reverse=rvs)
		return self
			
	def distinct(self, *cols):
		ret = sorted(self._records, key= itemgetter(*cols))
		self._records =  [next(l) for g, l in groupby(ret, key=itemgetter(*cols))]
		return self
	
	def update(self, where=lambda row:row, **set):
		for row in self._records:
			if not where(row):
				continue
			for k, func in set.items():
				row[k] = func(row)
		return self

	def group_by(self, column, **annotates): # annotates: field_name=func
		self._records.sort(key=itemgetter(column))
		ret = []
		for gname, lst in groupby(self._records, key=itemgetter(column)):
			lst = list(lst)
			dic = lst[0]
			for k, func in annotates.items():
				try:
					s = list(map(float, [e[k] for e in lst]))
				except:
					s = [e[k] for e in lst] 
				dic.update({'{}__{}'.format(k, func.__name__): func(s)})
			ret.append(dic)
		return ret
