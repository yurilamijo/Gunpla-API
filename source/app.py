from db import db
from flask import Flask
from flask_restful import Api

from resources.gunpla import Gunpla, GunplaList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'yuri'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Gunpla, '/gunpla/<string:name>')
api.add_resource(GunplaList, '/gunplas')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
    print('Gunpla API of Yuri Lamijo')