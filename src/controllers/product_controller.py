from src.models.product import Product
from src.models.price import Price
from app import db
from datetime import datetime

class ProductController:
    
    def find_all(self, filters=None):
        try:
            result = []

            products = Product.query.all()

            for row in products:
                row = self.__to_dict(row)
                get_price = Price.query.filter_by(product_id=row['source_product_id']).order_by(Price.updated_at.desc()).first()
                price = self.__to_dict(get_price)

                row['latest_price'] = price['price']
                result.append(row)

            db.session.commit()

            return self.__make_response(200, True, 'success', result)
        except Exception as err:
            db.session.rollback()
            return self.__make_response(500, False, str(err))
    
    def find_by_id(self, id):
        try:
            product = Product.query.get(id)
            
            resp = self.__make_response(404, True, 'product not found')
            
            if product:
                row = self.__to_dict(product)
                prices = Price.query.filter_by(product_id=row['source_product_id']).order_by(Price.updated_at.desc())
                
                get_price = Price.query.filter_by(product_id=row['source_product_id']).order_by(Price.updated_at.desc()).first()
                price = self.__to_dict(get_price)

                row['latest_price'] = price['price']
                row['prices'] = []

                for p in prices:
                    raw = self.__to_dict(p)
                    
                    row['prices'].append(raw)

                
                resp = self.__make_response(200, True, 'product found', row)
            
            db.session.commit()

            return resp
        except Exception as err:
            db.session.rollback()
            return self.__make_response(500, False, str(err))
    
    def find_by_product_id(self, product_id):
        try:
            product = Product.query.filter_by(source_product_id=product_id).first()
            
            resp = self.__make_response(404, True, 'product not found')
            
            if product:
                resp = self.__make_response(200, True, 'product found', self.__to_dict(product))
            
            db.session.commit()
            return resp
        except Exception as err:
            db.session.rollback()
            return self.__make_response(500, False, str(err))

    def create(self, data):
        try:
            product_price = data['price']

            data.pop("price", None)
            
            product = Product(**data)

            db.session.add(product)

            price_data = {
                "price": product_price,
                "product_id": data['source_product_id']
            }

            price = Price(**price_data)
            
            db.session.add(price)
            db.session.commit()

            return self.__make_response(201, True, 'created', {"id": product.id})

        except Exception as err:
            db.session.rollback()
            return self.__make_response(500, False, str(err))
        
        # db.session.close()
        

    def update(self, id, data):
        try:
            product = Product.query.get(id)

            product_price = data['price']

            data.pop("price", None)

            product.description = data['description']
            product.link = data['link']
            product.name = data['name']
            product.images = data['images']

            price_data = {
                "price": product_price,
                "product_id": data['source_product_id']
            }

            price = Price(**price_data)
            
            db.session.add(price)
            db.session.commit()

            return self.__make_response(200, True, 'created', {"id": id})

        except Exception as err:
            db.session.rollback()
            return self.__make_response(500, False, str(err))

    def delete(self, id):
        pass

    def __get_now(self):
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        
        return datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    def __make_response(self, code, status, message, data=None):
        response = {
            'code': code,
            'status': status,
            'message': message
        }

        if data:
            response['data'] = data

        return response

    def __to_dict(self, row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d
