import os
from flask import Flask
from flask import render_template
#from flask_login import LoginManager

def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=False,template_folder='templates',
        static_folder='static', static_url_path="/")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple index page that says hello
    @app.route('/')
    def index():
        return render_template('FoodRec.html')

    #from . import user
    #from . import stat
    #from . import recList
    
    from . import master
    from . import food

    #app.register_blueprint(user.bp)
    #app.register_blueprint(stat.bp)
    #app.register_blueprint(recList.bp)
    #app.register_blueprint(master.bp)
    app.register_blueprint(food.bp)

    

    
    return app