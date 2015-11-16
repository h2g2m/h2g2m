# -*- coding: utf-8 -*-
import unittest
import transaction

from pyramid import testing

from h2g2m.models import DBSession


class TestTxt(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine

        engine = create_engine('sqlite://')
        from h2g2m.models.tables import (
            Base,
            Usr,
            Txt,
        )

        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            creator = Usr(
                login='hitchhiker',
                nickname='hitchhiker',
                language='English',
                passwd='tester'
            )
            DBSession.add(creator)
            DBSession.flush()
            model = Txt(
                title='Calculus 1',
                authors='Gottfried Wilhelm Leibniz',
                edition='1',
                isbn='1337',
                creator=creator,
                language='English'
            )
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_add(self):
        from h2g2m.views.txt import add
        from h2g2m.models.tables import Usr

        request = testing.DummyRequest()
        request.usr = DBSession.query(Usr).first()
        info = add(request)
        self.assertIsNotNone(info['form'])
