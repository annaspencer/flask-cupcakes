"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

from models import db, connect_db, Cupcake


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "105-919-298"

connect_db(app)

@app.route('/')
def homepage():
    """cupcake homepage route"""

    return render_template("index.html")

@app.route('/api/cupcakes')
def get_cupcake():
    """returns cupcake data"""

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)
   

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """makes a cupcake in db"""
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """get specific cupcake data"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """updates a specific cupcake in db"""
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """deletes a single cupcake from db"""
    print("cupcake")

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    print(cupcake)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

