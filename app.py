from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    complaints = Complaint.query.all()
    return render_template('index.html', complaints=complaints)

@app.route('/add', methods=['POST'])
def add():
    new_complaint = Complaint(title=request.form['title'], content=request.form['content'], author=request.form['author'])
    db.session.add(new_complaint)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
