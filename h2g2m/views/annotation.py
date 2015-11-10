# -*- coding: utf-8 -*-
from h2g2m.events import AnnotationCreatedEvent, AnnotationEditedEvent, AnnotationDeletedEvent
from pyramid.path import AssetResolver
from pyramid.view import view_config
from ..lib.form import FormSchema, Isbn, IdExists
from ..lib.history import is_backworthy
from formencode import validators, All, ForEach
from pyramid_simpleform import Form
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPForbidden
from ..lib.repositories import LanguageRepository
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from ..lib.formrenderers import FormRenderer
from ..lib import helpers as h
from ..models import (DBSession, Annotation, Txt)


class AnnotationSchema(FormSchema):
    location = validators.String()
    content = validators.String(not_empty=True)
    language = validators.OneOf(LanguageRepository(
        AssetResolver('h2g2m').resolve('resources/en.json').abspath()
    ).find_all())
    title = validators.String()
    tex_header_id = validators.Int()  # TODO hier nur Ids erlauben von Tex-Headern, die dem aktuellen Benutzer gehören
    next = validators.OneOf(['list', 'view', 'edit'])
    courser_position = validators.Int(if_missing=None)
    focused_element = validators.Int(if_missing=None)


@view_config(
    route_name='annotation.add',
    renderer='../templates/annotation.form.pt',
)
def add(txt, request):
    if not request.usr:
        return HTTPForbidden()

    id = h.get_default_tex_header_id(request)
    obj = h.Struct(**{
        'tex_header_id': id,
    }) if id else None

    form = Form(request, AnnotationSchema, obj=obj)
    if form.validate():
        annotation = form.bind(
            Annotation(creator=request.usr),
            exclude=['next', 'courser_position', 'focused_element']
        )
        annotation.txt = txt
        request.bus.fire(AnnotationCreatedEvent(annotation=annotation))

        if form.data['next'] == 'view':
            location = request.route_url('annotation.view',
                                         txt_id=txt.id, annotation_id=annotation.id)
        elif form.data['next'] == 'edit':
            location = request.route_url(
                'annotation.edit',
                annotation_id=annotation.id,
                _query={
                    'courser_position': form.data['courser_position'],
                    'focused_element': form.data['focused_element']
                }
            )
        else:
            location = request.route_url('txt.view', txt_id=txt.id)
        return HTTPFound(location=location)
    return {'form': FormRenderer(form), 'txt': txt}


@view_config(
    route_name='annotation.edit',
    renderer='../templates/annotation.form.pt',
)
def edit(annotation, request):
    if not request.usr:
        return HTTPForbidden()
    form = Form(request, AnnotationSchema, obj=annotation)
    if form.validate():
        annotation = form.bind(annotation, exclude= \
            ['next', 'courser_position', 'focused_element'])
        request.bus.fire(AnnotationEditedEvent(annotation=annotation))
        if form.data['next'] == 'view':
            location = request.route_url(
                'annotation.view',
                annotation_id=request.matchdict['annotation_id']
            )
        elif form.data['next'] == 'edit':
            location = request.route_url(
                'annotation.edit',
                annotation_id=request.matchdict['annotation_id'],
                _query={
                    'courser_position': form.data['courser_position'],
                    'focused_element': form.data['focused_element']
                }
            )
        else:
            location = request.back_link
        return HTTPFound(location=location)
    return {'form': FormRenderer(form), 'annotation': annotation}


@view_config(
    route_name='annotation.delete',
)
def delete(annotation, request):
    if not request.usr:
        return HTTPForbidden()
    annotation = DBSession.query(Annotation).filter_by(id=request.matchdict['annotation_id']).one()
    # TODO: muessen wir hier wirklich die annotation neu aus der DB holen? genuegt vielleicht der Parameter?
    request.bus.fire(AnnotationDeletedEvent(annotation=annotation))
    return HTTPFound(request.back_link)


@view_config(
    route_name='annotation.view',
    renderer='../templates/annotation.view.pt',
)
@view_config(
    route_name='annotation.view',
    xhr=True, renderer='json',
)
@is_backworthy
def view(annotation, request):
    return {'annotation': annotation}


class ExportSchema(FormSchema):
    annotation_ids = ForEach(IdExists(Annotation))


@view_config(
    route_name='annotation.export',
    renderer='../templates/annotation.export.pt',
)
def annotation_export(request):
    form = Form(request, ExportSchema, method="GET")
    if form.validate():
        annotations = DBSession.query(Annotation).filter(Annotation.id.in_(form.data['annotation_ids'])).all()
        return {'annotations': annotations}
    return {}
