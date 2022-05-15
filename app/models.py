from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False,  unique=True)
    comment = db.relationship('Comment', backref='username', lazy='dynamic')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def set_password(self, password):
        pass_hash = generate_password_hash(password)
        self.password = pass_hash

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User: {self.username}'



class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_blogs(cls,id):
        blogs = Blog.query.filter_by(user_id = id).order_by(Blog.date_posted .desc()).all()
        return blogs

    @classmethod
    def get_all_blogs(cls):
        return Blog.query.order_by(Blog.date_posted ).all()

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String)
    comment_at = db.Column(db.DateTime)
    comment_by = db.Column(db.String)
    like_count = db.Column(db.Integer, default = 0)
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_comment(cls, id):
        gone = Comment.query.filter_by(id = id).first()
        db.session.delete(gone)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id = id).all()
        return comments        


    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # User like logic
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = BlogLike(user_id = self.id,blog_id = post.id)
            db.session.add(like)

    # User dislike logic
    def unlike_post(self, post):
        if self.has_liked_post(post):
            BlogLike.query.filter_by(
                user_id = self.id,
                blog_id = post.id).delete()

    # Check if user has liked post
    def has_liked_post(self, post):
        return BlogLike.query.filter(
            BlogLike.user_id == self.id,
            BlogLike.blog_id == post.id).count() > 0

    # string representaion to print out a row of a column, important in debugging
    def __repr__(self):
        return f"User {self.username}"


class Subscribers(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, index = True)

class BlogLike(db.Model):
    __tablename__ = "blog_like"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))


class Quote:
    """
    Blueprint class for quotes consumed from API
    """
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

    


