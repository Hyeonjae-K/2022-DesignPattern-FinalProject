from flask import Flask, render_template, request, redirect
import models

app = Flask(__name__)
con = models.DB('todo.db').getConnect()
cur = models.DB().getCursor()
do_table, schedule_table, delegate_table, dontdo_table = models.initTable(
    con, cur)


@app.route('/', methods=['GET'])
def index():
    dos = do_table.fetchAll()
    schedules = schedule_table.fetchAll()
    delegates = delegate_table.fetchAll()
    dontdos = dontdo_table.fetchAll()
    return render_template("index.html", dos=dos, schedules=schedules, delegates=delegates, dontdos=dontdos)


@app.route('/create/<string:table>', methods=['POST'])
def create(table):
    content = request.form['content']
    if table == 'do':
        do_table.insertData('content', content)
    elif table == 'schedule':
        schedule_table.insertData('content', content)
    elif table == 'delegate':
        delegate_table.insertData('content', content)
    elif table == 'dontdo':
        dontdo_table.insertData('content', content)
    return redirect('/')


@app.route('/delete/do/<int:id>')
def deleteDo(id):
    do_table.deleteData('id=%d' % id)
    return redirect('/')


@app.route('/delete/schedule/<int:id>')
def deleteSchedule(id):
    schedule_table.deleteData('id=%d' % id)
    return redirect('/')


@app.route('/delete/delegate/<int:id>')
def deleteDelegate(id):
    delegate_table.deleteData('id=%d' % id)
    return redirect('/')


@app.route('/delete/dontdo/<int:id>')
def deleteDontdo(id):
    dontdo_table.deleteData('id=%d' % id)
    return redirect('/')


@app.route('/update/do/<int:id>', methods=['GET', 'POST'])
def updateDo(id):
    if request.method == 'POST':
        do_table.updateData({'content': request.form['content']}, 'id=%d' % id)
        return redirect('/')
    else:
        return render_template('update.html', table='do', task=do_table.fetchOne('id=%d' % id))


@app.route('/update/schedule/<int:id>', methods=['GET', 'POST'])
def updateSchedule(id):
    if request.method == 'POST':
        schedule_table.updateData(
            {'content': request.form['content']}, 'id=%d' % id)
        return redirect('/')
    else:
        return render_template('update.html', table='schedule', task=schedule_table.fetchOne('id=%d' % id))


@app.route('/update/delegate/<int:id>', methods=['GET', 'POST'])
def updateDelegate(id):
    if request.method == 'POST':
        delegate_table.updateData(
            {'content': request.form['content']}, 'id=%d' % id)
        return redirect('/')
    else:
        return render_template('update.html', table='delegate', task=delegate_table.fetchOne('id=%d' % id))


@app.route('/update/dontdo/<int:id>', methods=['GET', 'POST'])
def updateDontdo(id):
    if request.method == 'POST':
        dontdo_table.updateData(
            {'content': request.form['content']}, 'id=%d' % id)
        return redirect('/')
    else:
        print(dontdo_table.fetchOne('id=%d' % id))
        return render_template('update.html', table='dontdo', task=dontdo_table.fetchOne('id=%d' % id))


if __name__ == "__main__":
    app.run(debug=True)
