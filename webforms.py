from wtfpeewee.orm import model_form
import wtforms
from webmodels import dynamic_models

def get_form(model):
    DynForm = model_form(model)
    return DynForm