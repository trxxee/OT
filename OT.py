from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import json
import hashlib

app = Flask(__name__)


def sample():
    return 1000;

app.secret_key = 'asdqw1321eif1j39j13f913u19u31jhdnkvnief9j19fjf13@#@'
users = dict()


@app.route('/', methods=['GET', 'POST'])
def main():
    if session.get('is_logined'):
        return render_template('main.html', name=session.get('name'))
    else:
        return render_template('login.html')
    return render_template('login.html')

def reply():
    if request.method == 'POST':
        reply = request.form['reply']

        #저장하기

        file = open('reply.json','w')
        file.write(json.dumps(replys))
        file.close()


        return redirect(url_for('main'))

    elif request.method == 'GET':
        return render_template('main.html')



@app.route('/login', methods=['post'])
def login():
    id = request.form['id']
    password = request.form['password']

    if users.get(id):
        password = hashlib.sha1((password+'salting value').encode('utf-8')).hexdigest()
        if users[id] == password:
            session['is_logined'] = True
            session['name'] = id
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error_msg='비밀번호가 일치하지 않습니다')
    else:
        return render_template('login.html', error_msg='아이디가 없습니다')


@app.route('/logout')
def logout():
    session['is_logined'] = False
    return redirect(url_for('main'))


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        re_password = request.form['re-password']

        if users.get(id):
            return render_template('join.html', error_msg='이미 아이디가 있습니다')

        if not password == re_password:
            return render_template('join.html', error_msg='비밀번호가 일치하지않습니다')


        users[id] = hashlib.sha1((password+'salting value').encode('utf-8')).hexdigest()

        #저장하기

        file = open('user.json','w')
        file.write(json.dumps(users))
        file.close()


        return redirect(url_for('main'))

    elif request.method == 'GET':
        return render_template('join.html')



@app.route('/hello/<name>')
def get_hello(name):
    return render_template('main.html', name=name)
def get_reply(reply):
    render_template('main.html', reply=reply)


if __name__ == '__main__':
    file = open('user.json')
    users = json.loads(file.read())

    file = open('reply.json')
    replys = json.loads(file.read())
    app.run(debug=True)
