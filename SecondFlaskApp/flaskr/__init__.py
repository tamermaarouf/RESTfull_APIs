# Import your dependencies
from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS, cross_origin
# Define the create_app function
def create_app(test_config=None):
# Create and configure the app
# Include the first parameter: Here, __name__is the name of the current Python module.

    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/plants', methods=['GET', 'POST'])
    def get_plants():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        plants = Plant.query.all()
        formatted_plants = [plants.format() for plant in plants]
        return jsonify({
            'success': True,
            'plants':formatted_plants[start:end],
            'total_plants':len(formatted_plants)
        })
    
    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    @app.route('/')
    # @cross_origin
    def hello_world():
        return jsonify({'message':'Hello, World'})

    @app.route('/smiley')
    def smiley():
        return ':)'
    # return the app instance
    return app
