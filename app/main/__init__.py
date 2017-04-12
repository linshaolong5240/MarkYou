# -*- coding: utf-8 -*-
from flask import Blueprint
blueprint_main = Blueprint('blueprint_main', __name__)

from . import views# at last
from ..models import Permission

@blueprint_main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
