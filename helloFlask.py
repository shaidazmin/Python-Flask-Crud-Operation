from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import redirect





app = Flask(__name__)  # creating the Flask class object

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    price = db.Column(db.String(20), nullable = False)
    time =  db.Column(db.DateTime, default = datetime.utcnow())


    def __repr__(self):
        return f"{self.title} - {self.price}"




@app.route('/', methods = ['GET', 'POST'])  # decorator drfines the
def home():

    if(request.method == "POST"):
        title = (request.form['title'])
        price = (request.form['price'])
        # insert product ...........
        product = Product(title=title, price=price)
        db.session.add(product)
        db.session.commit()

    # show products in list
    allProduct = Product.query.all()

    return render_template('index.html', allProduct = allProduct)


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    if(request.method == 'POST'):
        title = (request.form['title'])
        price = (request.form['price'])
        update_product = Product.query.filter_by(id=id).first()
        update_product.title = title
        update_product.price = price
        db.session.add(update_product)
        db.session.commit()
        return redirect('/')



    update_product = Product.query.filter_by(id=id).first()
    return render_template('update.html', update_product =  update_product)

@app.route('/delete/<int:id>')
def delete(id):
    product_id = Product.query.filter_by(id = id).first()
    db.session.delete(product_id)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=354)