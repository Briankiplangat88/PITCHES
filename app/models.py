from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage
from flask_login import UserMixin,current_user

from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    pitches = db.relationship("Pitches", backref="user", lazy="dynamic")
#  elationship('Comments',backref = 'user',lazy = "dynamic")   reviews = db.r
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)
    def save_pitches(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comments(cls,id):
        comments = Comments.query.filter_by(comment_id=id).all()
        return comments
    def __repr__(self):
        return f'User {self.username}'
class Pitches(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer,primary_key = True)
    pitch_id = db.Column(db.Integer)
    pitch_title = db.Column(db.String)
    pitch_category = db.Column(db.String)
    the_pitch = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comments', backref='pitch', lazy="dynamic")
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_pitches(cls, category):
        pitches= Pitches.query.filter_by(pitch_category=category)
        return pitches
    @classmethod
    def get_comments(cls,id):
        comments = Comments.query.filter_by(comment_id=id).all()
        return comments
    @classmethod
    def getPitchId(cls, id):
        pitch = Pitches.query.filter_by(id=id).first()
        return pitch
    @classmethod
    def clear_pitches(cls):
        Pitches.all_pitches.clear()
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment_id = db.Column(db.Integer)
    pitch_comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comments(cls,id):
        comments = comment = Comments.query.order_by(Comments.time_posted.desc()).filter_by(pitches_id=id).all()
        return comments
class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'
    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
