# -*- coding: utf-8 -*-
import os
import sys
import transaction
from sqlalchemy import engine_from_config
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from ..models import (
    Base,
    DBSession,
    Usr,
    Txt
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # Add users
        DBSession.add(Usr(nickname='frehse', login='frehse', passwd='tester2', language='Deutsch'))
        adm_usr = Usr(login='hitchhiker', nickname='hitchhiker', language='English', passwd='tester')
        DBSession.add(adm_usr)
        DBSession.flush()

        # Add texts
        DBSession.add(
            Txt(title='Analysis 1', edition='1', isbn='1337', creator=adm_usr, language='Deutsch',
                authors='Konrad Koenigsberger')
        )
        DBSession.add(
            Txt(title='Analysis 2', authors='Koenigsberger', edition='2', creator=adm_usr, language='English')
        )
        DBSession.add(
            Txt(title='Lineare Algebra 1', authors='Falko Lorenz', edition='1', creator=adm_usr, language='Deutsch')
        )
        DBSession.flush()
