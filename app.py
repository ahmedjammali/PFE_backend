from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from apis.users import user_blueprint


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '123456'  
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(user_blueprint, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
