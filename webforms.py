from wtfpeewee.orm import model_form, model_fields
import wtforms
from webmodels import dynamic_models

def get_form(model):
    #DynForm = model_form(model)
    fields = model_fields(model)
    for field in fields:
        pass
    return None