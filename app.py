from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


# Adicione isso no início do arquivo, após as importações
import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'name': request.form['name'],
            'lastname': request.form['lastname'],
            'age': request.form['age'],
            'city': request.form['city'],
            'address': request.form['address'],
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password']
        }

        if User.query.filter_by(username=user_data['username']).first():
            flash('Nome de usuário já existe!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=user_data['email']).first():
            flash('Email já cadastrado!', 'error')
            return redirect(url_for('register'))

        new_user = User(
            name=user_data['name'],
            lastname=user_data['lastname'],
            age=user_data['age'],
            city=user_data['city'],
            address=user_data['address'],
            email=user_data['email'],
            username=user_data['username']
        )
        new_user.set_password(user_data['password'])

        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Login inválido. Verifique usuário e senha.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)