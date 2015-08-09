# -*- coding: utf-8 -*-
from pyramid.view import view_config
from ..lib.form import FormSchema, IdExists
from formencode import validators, All, Any
from pyramid_simpleform import Form
from ..lib.formrenderers import FormRenderer
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPMovedPermanently, HTTPForbidden

from ..lib import helpers as h
from ..models import helpers as db

import re

from ..models import (
    DBSession,
    TexHeader,
    Post
)


@view_config(
    route_name='post.display',
    renderer='../templates/post.display.pt'
)
def view(post, request):
    return {'post': post}


def _form(post, annotation, request):
    defaults = {'tex_header_id': h.get_default_tex_header_id(request)}
    if post:
        defaults['parent_id'] = post.id
    if annotation:
        defaults['is_resolution'] = 1 if int(request.matchdict['is_resolution']) else 0
    form = Form(request, defaults=defaults, validators={
        'content': validators.String(not_empty=True),
        'is_resolution': validators.Bool(),
        'tex_header_id': All(validators.Int(),
                             Any(validators.Int(min=0, max=0), IdExists(TexHeader, usr=request.usr))),
        'parent_id': All(validators.Int(), IdExists(Post, if_missing=None))
    })
    if form.validate():
        post = form.bind(Post())
        post.creator_id = request.usr.id
        if annotation: post.annotation = annotation
        DBSession.add(post)
        DBSession.flush()
        request.session.flash(('success', u'Post successfully created.'))
        # return HTTPFound(location=request.route_url('annotation.view',
        # annotation_id=request.matchdict['annotation_id'],
        # txt_id=request.matchdict['txt_id']
        return HTTPFound(location=request.back_link)
    return {'form': FormRenderer(form), 'post': post}


@view_config(
    route_name='post.answer',
    renderer='../templates/post.answer.pt'
)
def answer(post, request):
    """ Post a new post which is the child of an already existing post. """
    return _form(post, None, request)

@view_config(
    route_name='post.create',
    renderer='../templates/post.answer.pt'
)
def creation(annotation, request):
    """ Post a new post which is the child of an annotation. """
    return _form(None, annotation, request)
