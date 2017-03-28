from flask import Blueprint

commit = Blueprint('commit', __name__)

from . import views
