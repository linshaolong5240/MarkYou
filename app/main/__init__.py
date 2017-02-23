# -*- coding: utf-8 -*-
from flask import Blueprint
blueprint_main = Blueprint('main', __name__)

from . import views# at last
