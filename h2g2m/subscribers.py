# -*- coding: utf-8 -*-
from pyramid import i18n
from formencode import api as formencode_api
from lib import helpers as h
from models import helpers as db
from pyramid.events import NewRequest, BeforeRender, ContextFound, NewResponse, subscriber

@subscriber(NewRequest)
def add_localizer(event):
    request = event.request
    localizer = i18n.get_localizer(request)
    if not hasattr(localizer, "old_translate"):
        localizer.old_translate = localizer.translate # Backup the default method
    request.localizer = localizer
    request.translate = lambda x: localizer.translate(i18n.TranslationString(x))

    # Set FormEncode language for this request
    formencode_api.set_stdtranslation(languages=["de"]) 
    # This should depend on the user's selection or whatever

    def multiple_gettext(value):
        # Try default translation first
        t = localizer.old_translate(i18n.TranslationString(value))
        if t == value:
            # It looks like translation failed, let's try FormEncode
            t = formencode_api._stdtrans(value)
        return t

    localizer.translate = multiple_gettext

@subscriber(BeforeRender)
def add_helper(event):
    event['h'] = h
    event['db'] = db

@subscriber(BeforeRender)
def add_menuitem(event):
    if not event['request']: return
    if event['request'].environ.has_key('menuitem'): 
        event['menuitem'] = event['request']['menuitem']
    else:
        p = event['request'].path[1:]
        i = p.find('/')
        event['menuitem'] = p[:i] if i!=-1 else p
