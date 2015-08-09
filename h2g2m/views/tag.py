# -*- coding: utf-8 -*-
from pyramid.view import view_config
from ..lib.form import FormSchema, IdExists
from formencode import validators, All, Any
from pyramid_simpleform import Form
from ..lib.formrenderers import FormRenderer
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPMovedPermanently

from ..lib import helpers as h
from ..models import helpers as db

import re

from ..models import (
    DBSession,
    TexHeader,
    Post
)

@view_config(
    route_name='tag', 
    renderer='../templates/tag.pt'
)
def view(tag,request):
    return { 'tag': tag }
