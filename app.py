from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'elite_rp_super_secret_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user', 'admin', 'owner'

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='На рассмотрении') # 'Принято', 'Отказано', 'Закрыто'
    author = db.Column(db.String(80))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    complaints = Complaint.query.all()
    return render_template('index.html', complaints=complaints)

@app.route('/create_complaint', methods=['POST'])
def create_complaint():
    if 'username' not in session: return redirect(url_for('login'))
    new_comp = Complaint(title=request.form['title'], content=request.form['content'], author=session['username'])
    db.session.add(new_comp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>/<status>')
def update_status(id, status):
    # Проверка на роль владельца (Shadow)
    if session.get('username') != 'Shadow': return "Доступ запрещен"
    comp = Complaint.query.get_or_404(id)
    comp.status = status
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pw = generate_password_hash(request.form['password'])
        # Назначаем владельца по нику
        role = 'owner' if request.form['username'] == 'Shadow' else 'user'
        new_user = User(username=request.form['username'], password=pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('index'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))