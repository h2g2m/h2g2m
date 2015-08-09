# -*- coding: utf-8 -*-
from pyramid.view import view_config

import formencode
from formencode import validators
from ..lib.form import FormSchema
from pyramid_simpleform import Form
from h2g2m.lib.formrenderers import FormRenderer
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPForbidden, HTTPFound

from ..lib import helpers as h

from ..models import (
    DBSession,
    Usr, Grp, TexHeader
)

# TODO: Bei allen admin_ - routinen einen standardview

def _login(request, location, msg=None):
    form = Form(request, LoginSchema)
    if form.validate():
        headers = remember(request, form.data['usr_id'],
                           max_age=60 * 60 * 24 * 365 if form.data['stay'] else None)
        # request.response.headerlist.extend(headers)
        if msg: request.session.flash(msg)
        return HTTPFound(location=location, headers=headers)
    return {'form': FormRenderer(form)}


class LoginSuccessful(validators.FancyValidator):
    credentials = None
    __unpackargs__ = ('*', 'credentials')

    messages = {
        'login_does_not_exist': 'User does not exist.',
        'wrong_passwd': 'Wrong password.',
    }

    def __init__(self, *args, **kw):
        super(validators.FancyValidator, self).__init__(*args, **kw)
        if len(self.credentials) != 2:
            raise TypeError('LoginSuccessful() requires login and password')

    def validate_python(self, field_dict, state):
        usr = DBSession.query(Usr).filter_by(login=field_dict[self.credentials[0]]).first()
        if not usr: raise formencode.Invalid(
            {self.credentials[0]: self.message('login_does_not_exist', state)},
            field_dict, state
        )
        if not usr.validate_passwd(field_dict[self.credentials[1]]):
            raise formencode.Invalid({self.credentials[1]: self.message('wrong_passwd', state)}, field_dict, state)
        field_dict['usr_id'] = usr.id


class LoginSchema(FormSchema):
    login = validators.String(not_empty=True)
    passwd = validators.String(not_empty=True)
    stay = validators.Bool()
    chained_validators = [LoginSuccessful('login', 'passwd')]


@view_config(
    route_name='login',
    renderer='../templates/login.pt',
)
def login(request):
    return _login(
        request,
        request.route_url('usr.loggedin'),
        ('success', u'Login successful.')
    )


@view_config(
    route_name='logout',
)
def logout(request):
    headers = forget(request)
    # request.response.headerlist.extend(headers)
    request.session.flash(('success', u'Logout successfull.'))
    return HTTPFound(
        location=request.route_url('home'),
        headers=headers)


class UniqueLogin(validators.FancyValidator):
    messages = {'username_exists': 'Username already exists.'}

    def validate_python(self, value, state):
        if DBSession.query(Usr).filter_by(login=value).first():
            raise formencode.Invalid(
                self.message('username_exists', state),
                value, state
            )
        return value


class RegisterSchema(FormSchema):
    login = formencode.All(UniqueLogin(), validators.String(not_empty=True))
    nickname = formencode.All(validators.String(not_empty=True))
    email = validators.Email()
    passwd = validators.String(not_empty=True)
    passwd_rep = validators.String(not_empty=True)
    chained_validators = [validators.FieldsMatch('passwd', 'passwd_rep')]


@view_config(
    route_name='register',
    renderer='../templates/register.pt',
)
def register(request):
    form = Form(request, RegisterSchema)
    if form.validate():
        grp = Grp(name=form.data['login'])
        DBSession.add(grp)
        DBSession.flush()

        usr = form.bind(
            Usr(default_language_id=request.current_language_id, grp_id=grp.id),
            include=['login', 'nickname', 'email', 'passwd']
        )
        DBSession.add(usr)
        DBSession.flush()
        headers = remember(request, usr.id)
        request.response.headerlist.extend(headers)

        request.session.flash(('success', u'Registration successful.'))
        return HTTPFound(
            location=request.route_url('usr.loggedin'),
            headers=headers
        )
    return {'form': FormRenderer(form)}


class UniqueLoginOrUnchanged(formencode.validators.FormValidator):
    __unpackargs__ = ('login_field', 'usr')
    messages = {'username_exists': 'Username already exists.'}

    def validate_python(self, value_dict, state):
        value = value_dict[self.login_field]
        if value == self.usr.login:
            return value_dict
        if DBSession.query(Usr).filter_by(login=value).first():
            raise formencode.Invalid(
                self.message('username_exists', state),
                value_dict, state,
                error_dict={self.login_field: formencode.Invalid( \
                    self.message('username_exists', state), \
                    value_dict, state)})


class EditSchema(FormSchema):
    login = validators.String(not_empty=True)
    nickname = validators.String(not_empty=True)
    email = validators.Email()

    def __init__(self, *args, **kwargs):
        self.chained_validators = [UniqueLoginOrUnchanged('login', kwargs['usr'])]


@view_config(
    route_name='usr.edit',
    renderer='../templates/profile.edit.pt',
)
def usr_edit(request):
    form = Form(request, EditSchema(usr=request.usr), obj=request.usr)
    if form.validate():
        form.bind(request.usr)
        DBSession.add(request.usr)
        request.session.flash(('success', u'Saved changes to profile.'))
        return HTTPFound(
            location=request.route_url('usr.view')
        )
    return {'usr': request.usr, 'form': FormRenderer(form)}


@view_config(
    route_name='usr.tags',
    renderer='../templates/profile.tags.pt',
)
def usr_tags(request):
    if not h.is_loggedin(request):
        return HTTPForbidden()
    return {'usr': request.usr}


@view_config(
    route_name='usr.annotations',
    renderer='../templates/profile.annotations.pt',
)
def usr_annotations(request):
    if not h.is_loggedin(request):
        return HTTPForbidden()
    return {'usr': request.usr}


@view_config(
    route_name='usr.texts',
    renderer='../templates/profile.texts.pt',
)
def usr_texts(request):
    if not h.is_loggedin(request):
        return HTTPForbidden()
    return {'usr': request.usr}


class PasswdSchema(FormSchema):
    passwd = validators.String(not_empty=True)
    passwd_rep = validators.String(not_empty=True)
    chained_validators = [validators.FieldsMatch('passwd', 'passwd_rep')]


@view_config(
    route_name='usr.passwd',
    renderer='../templates/profile.passwd.pt',
)
def usr_passwd(request):
    form = Form(request, PasswdSchema)
    if form.validate():
        form.bind(request.usr)
        DBSession.add(request.usr)
        request.session.flash(('success', u'Password successfully changed.'))
        return HTTPFound(
            location=request.route_url('usr.view')
        )

    return {'usr': request.usr, 'form': FormRenderer(form)}


@view_config(
    route_name='usr.view',
    renderer='../templates/profile.view.pt',
)
def usr_view(request):
    return {'usr': request.usr}


class TexHeaderSchema(FormSchema):
    name = validators.String(not_empty=True)
    action = validators.OneOf(['delete', 'not_delete'], if_missing='not_delete')
    content = validators.String(not_empty=True)
    is_default = validators.Bool(not_empty=True)
    tex_header_id = validators.Int(not_empty=True, if_missing=None)


@view_config(
    route_name='usr.tex_header',
    renderer='../templates/profile.tex_header.pt',
)
def usr_tex_header(request):
    if not h.is_loggedin(request):
        return HTTPForbidden()
    form = Form(request, TexHeaderSchema)
    if form.validate():
        if form.data['is_default']:
            tex_header = DBSession.query(TexHeader).filter_by(creator_id=request.usr.id)
            tex_header.update({'is_default': False})
        if form.data['tex_header_id'] == None:
            tex_header = form.bind(TexHeader())
            tex_header.creator = request.usr
            DBSession.add(tex_header)
        else:
            tex_header = DBSession.query(TexHeader).filter_by(id=form.data['tex_header_id']).one()
            if form.data['action'] == 'delete':
                DBSession.delete(tex_header)
            else:
                tex_header = form.bind(tex_header)
                DBSession.add(tex_header)
        return HTTPFound(location=request.route_url('usr.tex_header'))
    return {'usr': request.usr, 'form': FormRenderer(form)}
