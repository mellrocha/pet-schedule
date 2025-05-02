class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)          # Nome
    lastname = db.Column(db.String(50), nullable=False)      # Sobrenome
    age = db.Column(db.Integer, nullable=False)              # Idade
    city = db.Column(db.String(50), nullable=False)          # Cidade
    address = db.Column(db.String(100), nullable=False)      # Endereço
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)