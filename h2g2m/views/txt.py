# -*- coding: utf-8 -*-
from h2g2m.events import TxtCreatedEvent, TxtEditedEvent, TxtDeletedEvent
from pyramid.view import view_config
from ..lib.form import FormSchema, Isbn
from ..lib import helpers as h
from ..lib.history import is_backworthy
from ..lib.formrenderers import FormRenderer
from formencode import validators
from pyramid_simpleform import Form
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from ..lib.repositories import LanguageRepository
from pyramid.path import AssetResolver

from sqlalchemy import or_
from ..models import (
    DBSession,
    Txt,
    Person,
    Annotation,
)


class TxtSchema(FormSchema):
    authors = validators.String(not_empty=True)
    title = validators.String(not_empty=True)
    edition = validators.String()
    language = validators.OneOf(LanguageRepository(
        AssetResolver('h2g2m').resolve('resources/en.json').abspath()
    ).find_all())
    isbn = Isbn()
    url = validators.URL(add_http=True)


@view_config(
    route_name='txt.add',
    renderer='../templates/txt.form.pt'
)
def add(request):
    if not request.usr:
        return HTTPForbidden()
    # get last language (TODO this is slow)
    txts = [(t.language, t.creation_timestamp) for t in request.usr.txts]
    txts.sort(key=lambda x: x[1], reverse=True)

    obj = h.Struct(**{
        'language': txts[0][0] if txts else '',
    }) if id else None
    form = Form(request, TxtSchema, obj=obj)

    if form.validate():
        txt = form.bind(Txt(creator=request.usr))
        request.bus.fire(TxtCreatedEvent(txt=txt))
        return HTTPFound(location=request.route_url('txt.view', txt_id=txt.id))

    return {'form': FormRenderer(form)}


@view_config(
    route_name='txt.edit',
    renderer='../templates/txt.form.pt',
    # permission='write'
)
def edit(txt, request):
    if not request.usr:
        return HTTPForbidden()
    form = Form(request, TxtSchema, obj=txt)
    if form.validate():
        form.bind(txt)
        request.bus.fire(TxtEditedEvent(txt=txt))
        return HTTPFound(location=request.route_url('txt.view', txt_id=txt.id))
    return {'form': FormRenderer(form), 'txt': txt}


@view_config(
    route_name='txt.delete',
    # permission='write',
)
def delete(txt, request):
    if not request.usr:
        return HTTPForbidden()
    txt = DBSession.query(Txt).filter_by(id=request.matchdict['txt_id']).one()
    request.bus.fire(TxtDeletedEvent(txt=txt))
    return HTTPFound(location=request.route_url('txt.list'))


@view_config(
    route_name='txt.view',
    renderer='../templates/txt.view.pt',
    # permission='VIEW',
)
@is_backworthy
def view(txt, request):
    return {'txt': txt, 'txt_annotations': txt.annotations}


@view_config(
    route_name='txt.list',
    renderer='../templates/txt.list.pt',
)
@is_backworthy
def list(root_factory, request):
    return {'txts': DBSession.query(Txt)}


class BasicSearchSchema(FormSchema):
    q = validators.String(not_empty=True)


@view_config(
    route_name='txt.search.basic',
    renderer='../templates/txt.search.basic.pt'
)
def search_basic(request):
    form = Form(request, BasicSearchSchema)
    txts = []
    if form.validate():
        needle = '%' + form.data['q'] + '%'
        where = None
        where = or_(where, Txt.title.like(needle))
        where = or_(where, Txt.edition.like(needle))
        where = or_(where, Txt.isbn.like(needle))
        where = or_(where, Person.name.like(needle))
        txts = DBSession.query(Txt)
        txts = txts.outerjoin(Txt.author_list)
        txts = txts.filter(where)
    return {'txts': txts, 'form': FormRenderer(form)}


class AdvancedSearchSchema(FormSchema):
    author = validators.String()
    title = validators.String()
    isbn = Isbn()
    edition = validators.String()
    annotation_content = validators.String()


@view_config(
    route_name='txt.search.advanced',
    renderer='../templates/txt.search.advanced.pt'
)
def search_advanced(request):
    form = Form(request, AdvancedSearchSchema)
    txts = []
    if form.validate():
        txts = DBSession.query(Txt)
        if form.data['title']:
            txts = txts.filter(Txt.title.like('%' + form.data['title'] + '%'))
        if form.data['edition']:
            txts = txts.filter(Txt.edition.like('%' + form.data['edition'] + '%'))
        if form.data['isbn']:
            txts = txts.filter(Txt.isbn.like('%' + form.data['isbn'] + '%'))
        if form.data['author']:
            txts = txts.join(Txt.author_list).filter(Person.name.like('%' + form.data['author'] + '%'))
        if form.data['annotation_content']:
            txts = txts.join(Txt.annotations).filter(
                Annotation.content.like('%' + form.data['annotation_content'] + '%'))
    return {'txts': txts, 'form': FormRenderer(form)}


@view_config(
    route_name='txt.search.basic.toannotate',
    renderer='../templates/txt.search.basic.pt'
)
def search_basic_toannotate(annotation, request):
    ret = search_basic(request)
    ret['annotation'] = annotation
    return ret


@view_config(
    route_name='txt.search.advanced.toannotate',
    renderer='../templates/txt.search.advanced.pt'
)
def search_advanced_toannotate(annotation, request):
    ret = search_advanced(request)
    ret['annotation'] = annotation
    return ret
