from datetime import date

drugDB = \
{
	"7FTN10X":	{"code": "7FTN10X",   "name": "구연산펜타닐 주 500mcg/10ml"	,		"std_unit": "AMP"	,		"amount": 10	,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802283", "class": "마약", "component": "Fentanyl citrate 785μg"				, "shape": "주사제" },
	"7FTN2X":	{"code": "7FTN2X",   "name": "구연산펜타닐 주 100mcg/2ml"	,		"std_unit": "AMP"	,		"amount": 2		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802271", "class": "마약", "component": "Fentanyl citrate 157μg"				, "shape": "주사제" },
	"7FTN2XX":	{"code": "7FTN2XX",   "name": "구연산펜타닐 주 100mcg/2ml"	,		"std_unit": "AMP"	,		"amount": 2		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802273", "class": "마약", "component": "	Fentanyl citrate 157μg"				, "shape": "주사제" },
	"7FTN3X":	{"code": "7FTN3X",   "name": "구연산펜타닐 주 500mcg/10ml"	,		"std_unit": "AMP"	,		"amount": 10	,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802283", "class": "마약", "component": "Fentanyl citrate 785μg"				, "shape": "주사제" },
	"7FTNX"	:	{"code": "7FTNX",   "name": "구연산펜타닐 주 100mcg/2ml"	,		"std_unit": "AMP"	,		"amount": 2		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802271", "class": "마약", "component": "Fentanyl citrate 157μg"				, "shape": "주사제" },
	"7FTNXX":	{"code": "7FTNXX",   "name": "구연산펜타닐 주 100mcg/2ml"	,		"std_unit": "AMP"	,		"amount": 2		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802273", "class": "마약", "component": "	Fentanyl citrate 157μg"				, "shape": "주사제" },
	"7MOR15X":	{"code": "7MOR15X",   "name": "모르핀황산염주사 30mg/2ml"		,		"std_unit": "AMP"	,		"amount": 2		,		"amount_unit": "ml", "firm": "(주)비씨월드제약"	, "edi": "653101941", "class": "마약", "component": "Morphine Sulfate 15mg"				, "shape": "주사제" },
	"7MORPX":	{"code": "7MORPX",   "name": "모르핀황산염주사 5mg/5ml"		,		"std_unit": "AMP"	,		"amount": 5		,		"amount_unit": "ml", "firm": "(주)비씨월드제약"	, "edi": "653100841", "class": "마약", "component": "Morphine Sulfate 5mg"				, "shape": "주사제" },
	"7MORX"	:	{"code": "7MORX",   "name": "모르핀황산염주사 10mg/1ml"		,		"std_unit": "AMP"	,		"amount": 1		,		"amount_unit": "ml", "firm": "(주)비씨월드제약"	, "edi": "653101951", "class": "마약", "component": "morphine sulfate hydrate 10mg"		, "shape": "주사제" },
	"7MPX"	:	{"code": "7MPX",   "name": "염몰핀 주사 1ml"				,		"std_unit": "AMP"	,		"amount": 1		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657801481", "class": "마약", "component": "	Morphine HCl 10mg"					, "shape": "주사제" },
	"7PET1X":	{"code": "7PET1X",   "name": "염산페치딘 주사 1ml"			,		"std_unit": "AMP"	,		"amount": 1		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802751", "class": "마약", "component": "Pethidine HCl 50mg"					, "shape": "주사제" },
	"7PETX"	:	{"code": "7PETX",   "name": "염산페치딘 주사 1ml"			,		"std_unit": "AMP"	,		"amount": 1		,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657802751", "class": "마약", "component": "Pethidine HCl 50mg"					, "shape": "주사제" },
	"X-FENTA":	{"code": "FENTA",   "name": "펜타닐시트르산염주사 20ml"		,		"std_unit": "AMP"	,		"amount": 20	,		"amount_unit": "ml", "firm": "(주)비씨월드제약"	, "edi": "653100391", "class": "마약", "component": "Fentanyl citrate 157μg"				, "shape": "주사제" },
	"7RMV1"	:	{"code": "7RMV1",   "name": "레미바주1mg"					,		"std_unit": "VIAL"	,		"amount": 1		,		"amount_unit": "mg", "firm": "하나제약(주)"		, "edi": "657805381", "class": "마약", "component": "	remifentanil hydrochloride 1.1mg"	, "shape": "주사제" },
	"7ANP20X":	{"code": "7ANP20X",   "name": "아네폴 주 20ml"				,		"std_unit": "AMP"	,		"amount": 20	,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657804611", "class": "향정", "component": "Propofol 200mg"						, "shape": "주사제" },
	"7ANPX"	:	{"code": "7ANPX",   "name": "아네폴 주 12ml"				,		"std_unit": "AMP"	,		"amount": 12	,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657804591", "class": "향정", "component": "Propofol 10mg"						, "shape": "주사제" },
	"7ATB2X":	{"code": "7ATB2X",   "name": "아티반 주 2mg/0.5ml"			,		"std_unit": "AMP"	,		"amount": 0.5	,		"amount_unit": "ml", "firm": "일동제약(주)"		, "edi": "642901181", "class": "향정", "component": "	Lorazepam 2mg"						, "shape": "주사제" },
	"7DIAJEX":	{"code": "7DIAJEX",   "name": "삼진디아제팜 주 10mg/2ml"		,		"std_unit": "AMP"	,		"amount": 2		,		"amount_unit": "ml", "firm": "삼진제약(주)"		, "edi": "647800761", "class": "향정", "component": "Diazepam 10mg"						, "shape": "주사제" },
	"7KTM1X":	{"code": "7KTM1X",   "name": "케타민염산염 주사 50mg/5ml"	,		"std_unit": "AMP"	,		"amount": 5		,		"amount_unit": "ml", "firm": "(주)휴온스"		, "edi": "670604343", "class": "향정", "component": "Ketamine hydrochloride 288.4mg"		, "shape": "주사제" },
	"7MZL15":	{"code": "7MZL15",   "name": "미다컴 주 15mg/3ml"			,		"std_unit": "AMP"	,		"amount": 3		,		"amount_unit": "ml", "firm": "명문제약(주)"		, "edi": "649801721", "class": "향정", "component": "	Midazolam 15mg"						, "shape": "주사제" },
	"7MZL1X":	{"code": "7MZL1X",   "name": "미졸람 주 1mg/ml 5ml"		,		"std_unit": "AMP"	,		"amount": 5		,		"amount_unit": "ml", "firm": "(주)휴온스"		, "edi": "670605401", "class": "향정", "component": "Midazolam 5mg"						, "shape": "주사제" },
	"7MZL1X-A":	{"code": "7MZL1X",   "name": "미졸람 주 1mg/ml 5ml"		,		"std_unit": "AMP"	,		"amount": 5		,		"amount_unit": "ml", "firm": "(주)휴온스"		, "edi": "670605401", "class": "향정", "component": "Midazolam 5mg"						, "shape": "주사제" },
	"7MZLX"	:	{"code": "7MZLX",   "name": "미졸람 주 1mg/ml 5ml"			,		"std_unit": "AMP"	,		"amount": 5		,		"amount_unit": "ml", "firm": "(주)휴온스"		, "edi": "670605401", "class": "향정", "component": "Midazolam 5mg"						, "shape": "주사제" },
	"7NPIX"	:	{"code": "7NPIX",   "name": "날페인 주사 10mg/1ml"			,		"std_unit": "AMP"	,		"amount": 1		,		"amount_unit": "ml", "firm": "명문제약(주)"		, "edi": "649800051", "class": "향정", "component": "	Nalbuphine HCl 10mg"				, "shape": "주사제" },
	"7ANP20-X":	{"code": "7ANP20",   "name": "아네폴 주 12ml"				,		"std_unit": "AMP"	,		"amount": 12	,		"amount_unit": "ml", "firm": "하나제약(주)"		, "edi": "657804591", "class": "향정", "component": "Propofol 10mg"						, "shape": "주사제" },
	"7FRFX"	:	{"code": "7FRFX",   "name": "프리폴 엠시티주 12ml"			,		"std_unit": "VIAL"	,		"amount": 12	,		"amount_unit": "ml", "firm": "대원제약(주)"		, "edi": "671805073", "class": "향정", "component": "Propofol 10mg"						, "shape": "주사제" },
	"7FRFX-A":	{"code": "7FRFX",   "name": "프리폴 엠시티주 12ml"			,		"std_unit": "VIAL"	,		"amount": 12	,		"amount_unit": "ml", "firm": "대원제약(주)"		, "edi": "671805073", "class": "향정", "component": "Propofol 10mg"						, "shape": "주사제" },
	"7PTT1X":	{"code": "7PTT1X",   "name": "펜토탈소디움 주 0.5g"			,		"std_unit": "VIAL"	,		"amount": 0.5	,		"amount_unit": "g" , "firm": "JW중외제약(주)"	, "edi": "644912121", "class": "향정", "component": "Thiopental Sodium 500mg"				, "shape": "주사제" },
	"7PTTX"	:	{"code": "7PTTX",   "name": "펜토탈소디움 주 0.5g"			,		"std_unit": "VIAL"	,		"amount": 0.5	,		"amount_unit": "g" , "firm": "JW중외제약(주)"	, "edi": "644912121", "class": "향정", "component": "Thiopental Sodium 500mg"				, "shape": "주사제" },
}

reportElm = \
{
	"repoter" : {
		"name": "김철수",
		"birth": "1944-3-23",
		"tel" : "070-4665-9370",
		"assign_num" : "36호",
		"perm_class" : "마약류관리자",
		"market" : "에이치플러스양지병원",
		"region" : "서울",
		"address" : "관악구 남부순환로 1636 (신림동)"
	},

	"remainInfo" : {
		"date" : date.today().strftime("%Y-%m-%d"),
		"observer" : "원무과 강영진",
		"supervisor" : "약제과 최혜영",
		"place" : "에이치플러스양지병원약제과",
		"method" : "소각",
		"reason" : "재고관리 또는 보관을 하기에 곤란한 사유",
		"reasonDetail" : "잔여마약류"
	}
}

def get_dup_codes(drug_name):
	return [code for code, info in drugDB.items() if info['name'] == drug_name]

