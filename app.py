from flask import Flask , render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
	
db = SQLAlchemy(app)

# class for an item 
class Item(db.Model):
	# Defines the Table Name item
	__tablename__ = "item"

	# Makes three columns into the table id, description, price
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.Text(), nullable=False)
	description = db.Column(db.Text(), nullable=False)
	price = db.Column(db.Numeric(6,2), nullable=False)

	# A constructor function where we will pass the id, description and price and add as a new entry in the table.
	def __init__(self, name, description, price):
		self.name = name
		self.description = description
		self.price = price

	def __repr__(self):
		return "Item<id={} name={} description={} price={}>".format(self._id, self.name, self.description, self.price)

# class for image 
class Image(db.Model):
	# Defines the Table Name item
	__tablename__ = "image"
	
	# Makes two columns into the table
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.Text(), nullable=False)

	# A constructor function where we will pass the id and name of image and add as a new entry in the table.
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return "Image<id={} name={}>".format(self._id, self.name)

# Connect images to items
class Item_Image(db.Model):
	# Defines the Table Name item
	__tablename__ = "item_image"

	# Makes two columns into the table
	image_id = db.Column(db.Integer, ForeignKey("image._id"), primary_key=True)
	item_id = db.Column(db.Integer, ForeignKey("item._id"))

	def __init__(self, image_id, item_id):
		self.image_id = image_id
		self.item_id = item_id

	def __repr__(self):
		return "Item_Image<image_id={} item_id={}>".format(self.image_id, self.item_id)


# Control will come here and then gets redirect to the index function
@app.route("/")
def home():
	return redirect(url_for('index'))
  
@app.route("/index", methods = ["GET", "POST"])
def index():
	if request.method == 'POST': # When a user clicks submit button it will come here.
		data = request.form # request the data from the form in index.html fileee
		if "name" in data and "price" in data and "description" in data:
			name = data["name"]
			price = data["price"]
			description = data["description"]

			new_data = Item(name, description, price)
			db.session.add(new_data)
			db.session.commit()
		elif "image_name" in data:
			image_name = data["image_name"]

			new_image = Image(image_name)
			db.session.add(new_image)
			db.session.commit()
		elif "item_id" in data and "image_id" in data:
			image_id = data["image_id"]
			item_id = data["item_id"]
			

			new_data = Item_Image(image_id, item_id)
			db.session.add(new_data)
			db.session.commit()

		
	item_data = Item.query.all()
	image_data = Image.query.all()
	connection = Item_Image.query.all()

	return render_template("index.html", item_data = item_data, image_data = image_data, item_image_data = connection) # passes user_data variable into the index.html file.
	

if __name__=="__main__":
	db.create_all()
	app.run(debug=True, port=3000)