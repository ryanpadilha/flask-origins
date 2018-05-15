from flask import Blueprint, render_template, flash
from flask_login import login_required
from ..util.enums import FlashMessagesCategory


website = Blueprint('website', __name__)


@website.errorhandler(404)
def page_not_found(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('404.html'), 404


@website.errorhandler(500)
def internal_server_error(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('500.html'), 500


@website.errorhandler(Exception)
def unhandled_exception(e):
    flash(e, category=FlashMessagesCategory.ERROR.value)
    return render_template('500.html'), 500


@website.route('/')
@login_required
def index():
    return render_template('website/index.html')
