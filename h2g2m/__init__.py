# -*- coding: utf-8 -*-
from h2g2m.container import init_container
from h2g2m.lib.bus import Bus
from h2g2m.lib.dependencyinjection import Container
from h2g2m.listener import init_bus
from pyramid.config import Configurator
from pyramid.security import unauthenticated_userid
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

import lib.helpers as h
import models.helpers as db
from lib.history import Request, get_back_link

from .models import *
from models import helpers as modelhelpers

from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound

import sys

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    # Authentication and Authorization
    authentication_policy = AuthTktAuthenticationPolicy(
        secret='Ycf1Tjqe04MSTfIPYK63',
        callback=group_finder,
        include_ip=True
    )
    authorization_policy = ACLAuthorizationPolicy()

    # parse global_config
    settings['less_static_view'] = \
        ('less_static_view' in global_config) and \
        (global_config['less_static_view'].lower() in [True, 'true', 1])

    # Create config
    config = Configurator(
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        root_factory=RootFactory,
        request_factory=Request,
        settings=settings
    )

    reload(sys)
    sys.setdefaultencoding("UTF-8")
    config.add_settings(encoding="UTF-8")
    config.add_settings(default_encoding="UTF-8")

    # Properties
    config.set_request_property(get_back_link, 'back_link', reify=True)
    config.set_request_property(get_usr, 'usr', reify=True)
    config.set_request_property(lambda request: 1, 'current_language_id', reify=True) # TODO das hier irgendwie anders machen

    # Includes
    config.include('pyramid_beaker') # for sessions
    config.include('pyramid_mailer') # for mailing
    config.include('pyramid_chameleon') # for chameleon templates

    # static views
    if settings['less_static_view']:
        config.add_static_view('less', 'less', cache_max_age=3600)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # bus and container
    config.set_request_property(lambda request: init_bus(Bus()), 'bus', reify=True)
    config.set_request_property(lambda request: init_container(Container()), 'container', reify=True)

    # routes
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('contact', '/contact')

    # user
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('usr.loggedin', '/')
    config.add_route('register', '/register')

    config.add_route('usr.view',        '/profile/')
    config.add_route('usr.edit',        '/profile/edit')
    config.add_route('usr.passwd',      '/profile/passwd')
    config.add_route('usr.texts',       '/profile/texts')
    config.add_route('usr.annotations', '/profile/annotations')
    config.add_route('usr.tags',        '/profile/tags')
    config.add_route('usr.tex_header',  '/profile/tex_header')

    # tags
    config.add_route('tag', '/tg/{tag_id:\d+}',
        factory=FactoryFromID(Tag,'tag_id'))

    # txt routes
    config.add_route('txt.add', '/add')
    config.add_route('txt.list', '/list')
    config.add_route('txt.search.basic', '/search')
    config.add_route('txt.search.advanced', '/search/adv')
    config.add_route(
        'txt.search.basic.toannotate',
        '/a/{annotation_id:\d+}/search',
        factory=FactoryFromID(Annotation, 'annotation_id')
    )
    config.add_route(
        'txt.search.advanced.toannotate',
        '/a/{annotation_id:\d+}/search/adv',
        factory=FactoryFromID(Annotation, 'annotation_id')
    )
    config.add_route(
        'txt.view',
        '/t/{txt_id:\d+}',
        factory=FactoryFromID(Txt, 'txt_id')
    )
    config.add_route(
        'txt.edit',
        '/t/{txt_id:\d+}/edit',
        factory=FactoryFromID(Txt, 'txt_id')
    )
    config.add_route(
        'txt.delete',
        '/t/{txt_id:\d+}/delete',
        factory=FactoryFromID(Txt, 'txt_id')
    )

    # annotations 
    config.add_route(
        'annotation.add',
        '/t/{txt_id:\d+}/annotate',
        factory=FactoryFromID(Txt, 'txt_id')
    )
    config.add_route(
        'annotation.add_to_text',
        '/t/{txt_id:\d+}/annotate/existing/{annotation_id:\d+}',
        factory=FactoryFromID(Txt, 'txt_id')
    )
    config.add_route(
        'annotation.search.basic',
        '/t/{txt_id:\d+}/annotate/search',
        factory=FactoryFromID(Txt, 'txt_id')
    )
    config.add_route(
        'annotation.search.advanced',
        '/t/{txt_id:\d+}/annotate/search/adv',
        factory=FactoryFromID(Txt, 'txt_id')
    )
    config.add_route(
        'annotation.edit',
        '/a/{annotation_id:\d+}/edit/',
        factory=FactoryFromID(Annotation, 'annotation_id')
    )
    config.add_route(
        'annotation.delete',
        '/a/{annotation_id:\d+}/del/',
        factory=FactoryFromID(Annotation, 'annotation_id')
    )
    config.add_route(
        'annotation.view',
        '/a/{annotation_id:\d+}/',
        factory=FactoryFromID(Annotation, 'annotation_id')
    )
    config.add_route('annotation.export', '/annotations/export')

    # admin
    config.add_route('admin.usr.list', '/usrmanager')
    config.add_route(
        'admin.profile.edit',
        '/editprofile/{usr_id:\d+}/profile',
        factory=FactoryFromID(Usr,'usr_id')
    )
    config.add_route(
        'admin.edit.passwd',
        '/editprofile/{usr_id:\d+}/passwd',
        factory=FactoryFromID(Usr,'usr_id')
    )

    # posts
    config.add_route(
        'post.display',
        '/post/{post_id:\d+}/display',
        factory=FactoryFromID(Post,'post_id')
    )
    config.add_route(
        'post.answer',
        '/post/{post_id:\d+}/answer/retann/{annotation_id:\d+}',
        factory=FactoryFromID(Post,'post_id')
    )
    config.add_route(
        'post.create',
        '/post/create/ann/{annotation_id:\d+}/{is_resolution:\d+}',
        factory=FactoryFromID(Annotation,'annotation_id')
    )

    # internal routes
    config.add_route('language.json', '/language.json')

    # scan for views and go
    config.scan()

    return config.make_wsgi_app()



class RootFactory(object):
    __parent__ = None
    __name__ = ''

    def __init__(self, request):
        pass


def FactoryFromID(cls, param):
    def factory(request):
        try:
            obj = DBSession.query(cls).filter(cls.id==int(request.matchdict[param])).one()
            obj.__parent__ = RootFactory(request)
            obj.__name__ = None
            return obj
        except NoResultFound:
            raise HTTPNotFound
    return factory


def group_finder(user_id, request):
    usr = request.usr
    if usr is not None:
        l = [g.name for g in usr.groups]
        return l


def get_usr(request):
    # TODO: Sollten wir hier authenticated userid benutzen?
    usr_id = unauthenticated_userid(request)
    if usr_id is not None:
        return DBSession.query(Usr).filter_by(id=usr_id).first()
