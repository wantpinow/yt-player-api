from . import db, ma
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


# DEFINE MODELS
class User(db.Model):
    # Video information
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Created / updated time
    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        
        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user


class Video(db.Model):
    # Video information
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    author = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    thumbnail_url = db.Column(db.String(1000))
    progress = db.Column(db.Float)

    # User foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="videos")

    # Created / updated time
    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


# DEFINE SCHEMAS
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    videos = ma.auto_field()


class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        include_fk = True
