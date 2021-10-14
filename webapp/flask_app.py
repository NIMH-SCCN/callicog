import sys
sys.path.append('..')

from flask import Flask, _app_ctx_stack, render_template, request, redirect, url_for
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from database import DatabaseSession
from marmobox_schema import Protocol

db = DatabaseSession()

app = Flask(__name__)
CORS(app)
app.session = scoped_session(DatabaseSession, scopefunc=_app_ctx_stack.__ident_func__)

@app.route('/protocol/create', methods = ['GET', 'POST'])
def create():
	if request.method == 'GET':
		return render_template('create_protocol.html')
	if request.method == 'POST':
		protocol_name = request.form['protocol_name']

		protocol = Protocol(protocol_name=protocol_name)
		db.add(protocol)
		db.commit()
		return redirect('/protocol')

@app.route('/protocol')
def getProtocolList():
	protocols = db.query(Protocol).all()
	return render_template('protocol_list.html', protocols=protocols)

app.run(host='localhost', port=5000)
