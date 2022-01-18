from tabnanny import check
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from bbs.auth import login_required
from bbs.db import get_db
from bbs.bbs import get_post
from flask_paginate import Pagination, get_page_args

bp = Blueprint('post', __name__, url_prefix='/post')

def get_comment(comments,offset=0, per_page=10):
    return comments[offset: offset + per_page]

def get_comments(id):
    db = get_db()
    query="SELECT c.id, c.body, c.created, c.author_id, user.username, post_id FROM comment c JOIN post p ON c.post_id = p.id JOIN user ON c.author_id = user.id WHERE p.id = {a}".format(a=id)
    comments=db.execute(query).fetchall()
    return comments


@bp.route('/<int:id>')
def index(id):
    post=get_post(id,check_author=False)
    comments=get_comments(id) 
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(comments)
    pagination_comments = get_comment(comments,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap'
                           )
    return render_template('post/index.html',
                            post=post,
                           posts=pagination_comments,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           comments=comments
                           )

    #return render_template('post/index.html', post=post,comments=comments)

@bp.route('/<int:id>', methods=('GET', 'POST'))
@login_required
def add_comment(id):
    post=get_post(id,check_author=False)
    if request.method == 'POST':
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (post_id, body, author_id)'
                ' VALUES (?, ?, ?)',
                (id, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('post.index',id=id))

    return render_template('post/index.html',post=post)