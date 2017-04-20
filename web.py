from flask import Flask, render_template, abort, request, flash
from webmodels import dynamic_models, initialize
from webforms import get_form


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/entries/<int:entry_id>/', methods=['GET', 'POST'])
def edit_entry(entry_id):
    Entry = dynamic_models.get_models()[0]
    print Entry
    entry = Entry.get(Entry.id==entry_id)


    if request.method == 'POST':
        EntryForm = get_form(dynamic_models.get_models()[0])
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            form.populate_obj(entry)
            entry.save()
            flash('Your entry has been saved')
    else:
        EntryForm = get_form(dynamic_models.get_models()[0])
        form = EntryForm(obj=entry)

    return render_template('entry_edit.html', form=form, entry=entry)


if __name__ == "__main__":
    initialize()
    app.run()