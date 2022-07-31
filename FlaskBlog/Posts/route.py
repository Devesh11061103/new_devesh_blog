from flask import Blueprint, flash, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from FlaskBlog import db
from FlaskBlog.Posts.forms import PostForm
from FlaskBlog.models import Post

posts = Blueprint("posts", __name__)


@posts.route("/post-new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash("Your Post has been Created", "success")
        return redirect(url_for("main.home"))
    return render_template("newpost.html", title="New-Post", form=form, legend="Create Post")


@posts.route("/post/<int:post_id>")
def my_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been updated!", "success")
        return redirect(url_for("posts.my_post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("newpost.html", title="Update-Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been Deleted!", "success")
    return redirect(url_for("main.home"))
