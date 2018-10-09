from flask import render_template, request, url_for, redirect, flash, g
from flask_login import login_required
from app.main import bp
from .forms import SearchForm


@bp.route('/search/', methods={'GET', 'POST'})
# @login_required
def search():
    form = SearchForm()
    return render_template('search.html',
                           title="Search",
                           form=form)


@bp.route('/s/', methods={'GET', 'POST'})
# @login_required
def result():
    wd = request.args.get('wd')
    return render_template('result.html',
                           title="Search Result",
                           query=wd,
                           result=wd)