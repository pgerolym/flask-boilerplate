#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from functools import wraps
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# u = User.query.get(1)
# u.set_password('test')
# db_session.commit()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager(app=app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Automatically tear down SQLAlchemy.
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# Login required decorator.
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Παρακαλώ πρώτα συνδεθείτε.')
            return redirect(url_for('login'))
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/PTOdashboard')
@login_required
def PTOdashboard():
    return render_template('pages/placeholder.about.html', username=current_user.name)

@app.route('/PTOperTeacher')
@login_required
def PTOperTeacher():
    return render_template('pages/placeholder.about.html', username=current_user.name)

@app.route('/PTOnewRecord')
@login_required
def PTOnewRecord():
    return render_template('pages/placeholder.about.html', username=current_user.name)

@app.route('/PTOupdateRecord')
@login_required
def PTOupdateRecord():
    return render_template('pages/placeholder.about.html', username=current_user.name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        email = form.email.data

        # remember = True if form.remember else False
        
        user = User.query.filter_by(email=email).first()
        # Login and validate the user.
        # user should be an instance of your `User` class
        
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Παρακαλώ διορθώστε τα στοιχεία εισόδου και προσπαθήστε ξανά.')
            return redirect(url_for('login'))  

        login_user(user)
        print(session.keys)
        flash('Είσοδος επιτυχής.')
        
        # next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return abort(400)

        return redirect(url_for('home'))
    
    return render_template('forms/login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
