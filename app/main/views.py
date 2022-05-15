from flask import (render_template, request, redirect, url_for, abort, flash)
from . import main
from ..models import Blog, User, Comment, Subscribers
from flask_login import login_required, current_user
from .forms import (UpdateProfile, BlogForm, CommentForm, UpdateBlogForm)
from datetime import datetime
from .. import db
from ..requests import get_quote
from ..email import welcome_message, notification_message

@main.route('/')
def index():
    blogs = Blog.get_all_blogs()
    quote = get_quote()

    if request.method == "POST":
        new_sub = Subscribers(email = request.form.get("subscriber"))
        db.session.add(new_sub)
        db.session.commit()
        welcome_message("Thank you for subscribing to the Hands On", "email/welcome", new_sub.email)
    return render_template('index.html', quote = quote, blog = blogs)

# about
@main.route('/about')
def about():
    return render_template('about.html')

# blog posts
@main.route("/blog/<int:id>", methods = ["POST", "GET"])
def blog(id):
    blog = Blog.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(blog_id = id).all()
    comment_form = CommentForm()
    comment_count = len(comments)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        comment_form.comment.data = ""
        comment_alias = comment_form.alias.data
        comment_form.alias.data = ""
        if current_user.is_authenticated:
            comment_alias = current_user.username
        new_comment = Comment(comment = comment, 
                            comment_at = datetime.now(),
                            comment_by = comment_alias,
                            blog_id = id)
        new_comment.save_comment()
        return redirect(url_for("main.blog", id = blog.id))

# delete comment
@main.route("/blog/<int:id>/<int:comment_id>/delete")
def delete_comment(id, comment_id):
    blog = Blog.query.filter_by(id = id).first()
    comment = Comment.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("main.blog", id = blog.id))

#  new blog post
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
        db.session.add(new_blog)
        db.session.commit()
        subs = Subscribers.query_all()
        for sub in subs:
            notification_message(blog_title, "email/notification", sub.email, new_blog = new_blog)
            pass
        return redirect(url_for("main.blog", id = new_blog.id))
    
    return render_template('newblog.html', title='New Blog', blog_form=blog_form)

# edit or update blog post
@main.route("/blog/<int:id>/update", methods = ["POST", "GET"])
@login_required
def edit_post(id):
    blog = Blog.query.filter_by(id = id).first()
    edit_form = UpdateBlogForm()

    if edit_form.validate_on_submit():
        blog.blog_title = edit_form.title.data
        edit_form.title.data = ""
        blog.blog_content = edit_form.content.data
        edit_form.content.data = ""

        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("main.blog", id = blog.id))

    return render_template("editblogpost.html", blog = blog, edit_form = edit_form)

   