# -*- coding: utf-8 -*-
from peewee import Proxy, SqliteDatabase, Model, CharField, BigIntegerField, FloatField, DateTimeField,TextField
from unidecode import unidecode
import json
database_proxy = Proxy()

# sqlite_db = SqliteDatabase('excels.db',  fields={'primary_key': 'INTEGER AUTOINCREMENT'})
sqlite_db = SqliteDatabase('excels.db')

class DynMo(object):
    def __init__(self):
        self.dynamic_models = []
        self.dynamic_forms = []

    def get_models(self):
        return self.dynamic_models

    def add_model(self,model):
        self.dynamic_models.append(model)

    def get_forms(self):
        return self.dynamic_forms

    def add_form(self, wtform):
        self.dynamic_forms.append(wtform)


class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = sqlite_db


class XlsTable(BaseModel):
    name = CharField()
    friendly_name = CharField()
    data = TextField()
    filexls = CharField()
    cursor = CharField()
    class Meta:
        db_table = "xlstable"

def factory(data):
    FactMod = type(unidecode(data["name"]), (BaseModel,), {})
    for field in data["fields"]:
        fieldtype = None
        if "str" in field["datatype"]:
            fieldtype = CharField
        elif "int" in field["datatype"]:
            fieldtype = BigIntegerField
        elif "float" in field["datatype"]:
            fieldtype = FloatField
        elif "datetime" in field["datatype"]:
            fieldtype = DateTimeField

        if fieldtype:
            fieldtype().add_to_class(FactMod, unidecode(field["title"].replace(" ", "_").replace(".","")))

    sqlite_db.create_table(FactMod, safe=True)
    return FactMod


def initialize():
    print "create DB"
    try:

        database_proxy.initialize(sqlite_db)
        sqlite_db.connect()
        sqlite_db.create_tables([XlsTable], safe=True)
        for table in XlsTable.select():
            dynamic_models.add_model(factory(json.loads(table.data)))
        sqlite_db.close()
        print dynamic_models
        return dynamic_models
    except:
        pass

def create_table(model):
    sqlite_db.create_tables([model], safe=True)

def create_model(data):
    try:
        model = XlsTable.get(XlsTable.name == data["name"])
    except:
        model = XlsTable()
        model.name = data["name"]
        model.friendly_name = data["name"]
        model.data = json.dumps(data)
        model.filexls = data["filexls"]
        model.cursor = data["cursor"]
        model.save()
    mem_model = factory(json.loads(model.data))
    dynamic_models.add_model(mem_model)
    return mem_model

dynamic_models = DynMo()
