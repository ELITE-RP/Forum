import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='На рассмотрении')
    author = db.Column(db.String(80), nullable=False)
    image_filename = db.Column(db.String(120))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', complaints=Complaint.query.all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pw = generate_password_hash(request.form['password'])
        role = 'owner' if request.form['username'] == 'Shadow' else 'user'
        db.session.add(User(username=request.form['username'], password_hash=pw, role=role))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            session.update({'user_id': user.id, 'username': user.username, 'role': user.role})
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/add', methods=['POST'])
def add_complaint():
    if 'user_id' not in session: return redirect(url_for('login'))
    file = request.files.get('image')
    filename = secure_filename(file.filename) if file else None
    if filename:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.session.add(Complaint(title=request.form['title'], content=request.form['content'], 
                             author=session.get('username'), image_filename=filename))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>/<status>')
def update(id, status):
    if session.get('role') in ['owner', 'admin']:
        c = Complaint.query.get_or_404(id)
        c.status = status
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
