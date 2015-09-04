import json
from pyexcel_ods import get_data

def reader_ods(ods_path,planilha):
	data = get_data(ods_path)
	arquivo = json.dumps(data)
	jarq = json.loads(arquivo)
	return jarq[planilha]
