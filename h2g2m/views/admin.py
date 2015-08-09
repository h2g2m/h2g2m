# -*- coding: utf-8 -*-
from pyramid.view import view_config

from ..models import (
    DBSession,
    Usr
)


@view_config(
    route_name='admin.usr.list',
    renderer='../templates/usrmanager.pt',
)
def usrmanager(request):
    return {'usrs': DBSession.query(Usr)}
