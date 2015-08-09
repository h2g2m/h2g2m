# -*- coding: utf-8 -*-
from pyramid.view import view_config

from h2g2m.lib.logstream import get_logstream

from ..models import (
    DBSession,
    Usr,
    Txt,
    Annotation,
)


@view_config(
    route_name='home',
    renderer='../templates/home.pt'
)
def home(request):
    # Create Statistics
    stats = {
        'users': DBSession.query(Usr).count(),
        'texts': DBSession.query(Txt).count(),
        'annotations': DBSession.query(Annotation).count()
    }

    return {'log': get_logstream(request), 'stats': stats}
