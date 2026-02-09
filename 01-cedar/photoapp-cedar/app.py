import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, AnonymousUserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, UTC, date
from dotenv import load_dotenv
from cedar_auth import check_authorization

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Use environment variables with fallbacks
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///photoapp.db')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Make check_authorization available in templates
@app.context_processor
def utility_processor():
    return dict(check_authorization=check_authorization)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    birthday = db.Column(db.Date, nullable=False)
    images = db.relationship('Image', backref='user', lazy=True)

    def age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def is_minor(self):
        return self.age() < 18


class GuestUser(AnonymousUserMixin):   
    id = "guest"
    is_admin = False
    
    def is_minor(self):
        return True

    
login_manager.anonymous_user = GuestUser

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    is_explicit = db.Column(db.Boolean, default=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    public_images = Image.query.filter_by(is_public=True).order_by(Image.upload_date.desc()).all()
    return render_template('index.html', images=public_images)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d').date()
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=username, 
            password_hash=generate_password_hash(password),
            birthday=birthday
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_images = Image.query.filter_by(user_id=current_user.id).order_by(Image.upload_date.desc()).all()
    return render_template('dashboard.html', images=user_images)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'image' not in request.files:
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    file = request.files['image']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        is_public = 'is_public' in request.form
        is_explicit = 'is_explicit' in request.form
        
        image = Image(
            filename=filename,
            is_public=is_public,
            is_explicit=is_explicit,
            user_id=current_user.id
        )
        db.session.add(image)
        db.session.commit()
        
        flash('Image uploaded successfully!')
    else:
        flash('Invalid file type')
    
    return redirect(url_for('dashboard'))

@app.route('/toggle_visibility/<int:image_id>')
@login_required
def toggle_visibility(image_id):
    image = Image.query.get_or_404(image_id)
    if not check_authorization(current_user, "delete", image):
        flash('Unauthorized action')
        return redirect(url_for('dashboard'))
    
    image.is_public = not image.is_public
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/user/<username>')
def user_public_images(username):
    user = User.query.filter_by(username=username).first_or_404()
    public_images = Image.query.filter_by(user_id=user.id, is_public=True).order_by(Image.upload_date.desc()).all()
    return render_template('user_images.html', user=user, images=public_images)

@app.route('/images/<filename>')
def serve_image(filename):
    image = Image.query.filter_by(filename=filename).first_or_404()
    
    if not check_authorization(current_user, "view", image):
        abort(403)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_image/<int:image_id>')
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    if not check_authorization(current_user, "delete", image):
        abort(403)
    
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    except OSError:
        pass
    
    # Delete the database record
    db.session.delete(image)
    db.session.commit()
    
    flash('Image deleted successfully!')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin'),
                is_admin=True,
                birthday=date(1980, 1, 1)  # Dummy birthday for admin
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True) 