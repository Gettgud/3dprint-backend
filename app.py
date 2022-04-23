
from flask import Flask , render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://majfielwtbzupo:678b932034546ee4c7d8906512704b8f00df3e311ee650d4355ae0da02656a21@ec2-44-199-143-43.compute-1.amazonaws.com:5432/dcm34gl41nh898'
	
db = SQLAlchemy(app)

class User(db.Model):
	# Defines the Table Name user
	__tablename__ = "user"

	# Makes three columns into the table id, name, email
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)

	# A constructor function where we will pass the name and email of a user and it gets add as a new entry in the table.
	def __init__(self, name, email):
		self.name = name
		self.email = email

# Control will come here and then gets redirect to the index function
@app.route("/")
def home():
	return redirect(url_for('index'))


@app.route("/index", methods = ["GET", "POST"])
def index():
	if request.method == 'POST': # When a user clicks submit button it will come here.
		data = request.form # request the data from the form in index.html file
		name = data["name"]
		email = data["email"]

		new_data = User(name, email)
		db.session.add(new_data)
		db.session.commit()

		user_data = User.query.all()

		return render_template("index.html", user_data = user_data) # passes user_data variable into the index.html file.

	return render_template("index.html")
	

if __name__=="__main__":
	db.create_all()
	app.run(debug=True)