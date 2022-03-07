from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, passwd):
        self.password_hash = bcrypt.generate_password_hash(passwd).decode('utf-8')

    def check_password(self, passwd):
        return bcrypt.check_password_hash(self.password_hash, passwd)

    def __repr__(self):
        return f'<User {self.username}>'
