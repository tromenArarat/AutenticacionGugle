from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
import os

app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# Cookies config
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Permitir cookies de terceros
app.config['SESSION_COOKIE_SECURE'] = True  # Solo enviar en conexiones seguras (https)

# Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
from werkzeug.security import generate_password_hash

class User(db.Model):
    """User Model

    Args:
        db (_type_): Model from SQL Alchemy

    Returns:
        string: Only check_password returns, else used to store user info
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



@app.route('/')
def home():
    """Displays a Page based on the session of the current user

    Returns:
        html template: Returns the Dashboard or Index
    """
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Confirms username and password in the database using the model

    Returns:
        html template: Directs the user to a page matching their login info
    """
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', error='Invalid username or password.')

@app.route('/register', methods=['POST'])
def register():
    """Registers a new user within the SQL Alchemy DB

    Returns:
        html template: Creates a session with the new user
    """
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('index.html', error='Username already exists.')
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Google Login
@app.route('/login/google')
def login_google():
    try:
        redirect_uri = url_for('authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error(f"Error during Google login: {str(e)}")
        return "Error during Google login", 500

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    userinfo_endpoint = google.server_metadata["userinfo_endpoint"] 
    resp = google.get(userinfo_endpoint)
    user_info = resp.json()
    username = user_info['email']
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        #password = os.urandom(24).hex()
        #user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['oauth_token'] = token

        return redirect(url_for('dashboard'))

    session['username'] = username
    session['oauth_token'] = token

    return redirect(url_for('dashboard'))



# Authorize for Google

@app.route('/reset_cache')
def reset_cache():
    # Clear all session data
    session.clear() 
    # Optionally, redirect the user to the login page or home page
    return redirect(url_for('login'))




if __name__ == '__main__':
    # Create a db and table
    with app.app_context():
        #db.drop_all()  # Drop all tables
        db.create_all()
        app.run(debug=True)
