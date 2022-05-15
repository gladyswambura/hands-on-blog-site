from flask import (render_template, request, redirect, url_for, abort, flash)
from . import main
from ..models import Blog, User, Comment, Post, Subscribers
from flask_login import login_required, current_user
from .forms import (UpdateProfile, BlogForm, CommentForm, UpdateBLogForm)
from datetime import datetime
from .. import db
from ..requests import get_quote
from ..email import welcome_message, notification_message

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/newblog', methods=['POST', 'GET'])
@login_required
def new_blog():
    blog_form= BlogForm()
    if blog_form.validate_on_submit():
        flash('Your post has been created', 'success')
        blog_title = blog_form.title.data
        blog_form.title.data = ""
        blog_content = blog_form.content.data 
        blog_form.content.data = ""
        new_blog = Blog(blog_title = blog_title,
                        blog_content = blog_content,
                        posted_at = datetime.now(),
                        blog_by = current_user.username,
                        user_id = current_user.id)
        new_blog.save_blog()
        subs = Subscribers.query.all()
        for sub in subs:
            notification_message(blog_title, "email/notification", sub.email, new_blog = new_blog)
            pass
        return redirect(url_for("main.blog", id = new_blog.id))
    
    return render_template('newblog.html', title='New Blog', blog_form=blog_form)

   