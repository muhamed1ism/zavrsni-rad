from flask import jsonify, Blueprint

home_bp = Blueprint('home', __name__)


# Home
@home_bp.route('/', methods=['GET'])
def home():
    return jsonify(msg='Doctor service is up and running.'), 200
