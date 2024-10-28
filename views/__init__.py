from flask import Blueprint

app_views = Blueprint('app_views', __name__)

# Import all routes AFTER creating the blueprint
from views.views import *
from views.guest import *
from views.email import *
from views.dashboard import *
from views.profile import *
from views.vendors import *
from views.auth import *
