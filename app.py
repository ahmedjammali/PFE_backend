from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from apis.users import user_blueprint
from apis.team import team_blueprint
from apis.privilege import privilege_blueprint
from apis.folder import Folder_blueprint
from apis.files import Files_blueprint
from apis.GoogleDoc import doc_blueprint


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '123456'  
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(team_blueprint , url_prefix = '/team')
app.register_blueprint(privilege_blueprint, url_prefix='/privilege' )
app.register_blueprint(Folder_blueprint ,url_prefix='/folder')
app.register_blueprint(Files_blueprint ,url_prefix='/files')
app.register_blueprint(doc_blueprint ,url_prefix='/drive')

if __name__ == '__main__':
    app.run(debug=True)
