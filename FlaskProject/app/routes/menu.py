from flask import Blueprint, render_template

bp = Blueprint('menu', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('menu.html')
