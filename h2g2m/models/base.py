# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker
from h2g2m.lib.dbversioning import versioned_session

SessionMaker = sessionmaker(extension=ZopeTransactionExtension())
DBSession = scoped_session(SessionMaker)
versioned_session(DBSession)
Base = declarative_base()
