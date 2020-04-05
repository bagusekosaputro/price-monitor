from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_product_id = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.Text, nullable=True)
    prices = db.relationship('Price', backref="product", lazy=True)
    images = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.name

