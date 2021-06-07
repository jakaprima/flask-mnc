from flask import Flask
from markupsafe import escape
app = Flask(__name__)
from flask import Blueprint, render_template

root = Blueprint('root', __name__)


@root.route('/')
def index():
    return {
        'api': 'v1'
    }
