from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from bbs.db import get_db
from flask_paginate import Pagination, get_page_args

bp = Blueprint('profile', __name__, url_prefix='/profile')

def get_posts(posts,offset=0, per_page=10):
    return posts[offset: offset + per_page]

@bp.route('/<int:id>')
def person(id):
    #return f'{username}\'s profile'
    posts = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?',
        (id,)
    ).fetchall()
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(posts)
    pagination_posts = get_posts(posts,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap'
                           )
    return render_template('profile/person.html',
                            name=id,
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
    return render_template('profile/person.html',name=id, posts=post)

