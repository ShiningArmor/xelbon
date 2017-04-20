from openpyxl import load_workbook
from utils import xls2xlsx, index2excel
import json

class ExcelConnector(object):
    def __init__(self, pathfile, mode="r"):
        self.pathfile = pathfile
        self.open_mode = mode
        self.table_index = 0
        self.wb = None
        self.tables = []
        self.open()
        self.initialize()

    def open(self):
        readonly = True if self.open_mode == "r" else False
        if self.pathfile[self.pathfile.rfind("."):] == ".xls":
            self.wb = xls2xlsx(self.pathfile)
        elif self.pathfile[self.pathfile.rfind("."):] == ".xlsx":
            self.wb = load_workbook(filename=self.pathfile, read_only=readonly)

    def initialize(self):
        sheets_names = self.wb.get_sheet_names()
        for idx, sheet in enumerate(sheets_names):
            table = Table(self.get_sheet(idx),idx)
            self.tables.append(table)

    def set_table_crusors(self):
        for table in self.tables:
            table.set_cursor()

    def get_sheet(self, i):
        return  self.wb[self.wb.get_sheet_names()[i]]

class Table(object):
    def __init__(self, sheet_obj, index):
        self.sheet = sheet_obj
        self.name = self.sheet.title
        self.wb_index = index
        self.dimensions = self.sheet.dimensions
        self.indexes = self.find_table()
        self.cursor = [0, 0]

    def set_cursor(self):
        self.cursor = [self.indexes[0]["column"], len(self.sheet[self.indexes[0]["column"]]) + 1]

    def refresh(self):
        pass

    def find_table(self):
        stop = False
        indexes = []
        for row in self.sheet.rows:
            for i in row:
                if i.value:
                    indexes.append({"title": i.value,
                                    "column": i.column,
                                    "row": i.row,
                                    "datatype": str(type(self.sheet[index2excel(i.row  + 1 , i.col_idx)].value))
                                   })
                    stop = True
            if stop:
                break
        return indexes

    def export(self):
        return json.dumps(dict(
            name= self.name,
            filexls=self.sheet.title,
            cursor=self.cursor,
            fields=self.indexes
        ))