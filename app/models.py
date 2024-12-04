from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def is_active(self):
        return True 
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    
from app import login_manager
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))