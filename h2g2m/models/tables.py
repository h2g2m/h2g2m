# -*- coding: utf-8 -*-
from abc import abstractmethod
import hashlib
import helpers
from sqlalchemy import Text, DateTime, func
from sqlalchemy.orm.exc import NoResultFound
from h2g2m.lib.dbversioning import Versioned
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.schema import ForeignKey
from base import Base, DBSession
from mixins import DefaultTableMixin, TexHeadered


def get_or_create(obj, cls, name):
    with DBSession.no_autoflush:
        # print 'START', obj, get_state(obj), cls, name
        # is_pend = is_pending(obj)
        # if is_pend: DBSession.expunge(obj)

        try:
            res = DBSession.query(cls).filter_by(name=name).one()
        except NoResultFound:
            res = cls(name=name)
            # DBSession.add(res)
            # DBSession.flush()

        # if is_pend: DBSession.add(obj)
        # print 'END', obj, get_state(obj), cls, name
        return res


def get_or_create_language(obj, language_name):
    return get_or_create(obj, Language, language_name)


class Language(DefaultTableMixin, Base):
    shortcut = Column(Text, nullable=True)
    name = Column(Text, nullable=False)


class Usr(DefaultTableMixin, Base):
    # a unique string used only to login, can be replaced by open-id later
    login = Column(Text, nullable=False, unique=True)
    # the nickname displayed to other users
    nickname = Column(Text, nullable=False)
    passwd_salt = Column(Text, nullable=False)
    passwd_hash = Column(Text, nullable=False)
    email = Column(Text)
    creation_timestamp = Column(DateTime, nullable=False, default=func.now())
    default_language_id = Column(Integer, ForeignKey(Language.id), nullable=False)

    def get_salted_passwd_hash(self, passwd, salt=False):
        if not salt:
            if not self.passwd_salt: self.passwd_salt = helpers.gen_salt()
            salt = self.passwd_salt
        return hashlib.sha256('%s%s' % (passwd, salt)).hexdigest()

    @property
    @abstractmethod
    def passwd(self):
        pass

    @passwd.setter
    def passwd(self, passwd):
        self.passwd_hash = self.get_salted_passwd_hash(passwd)

    def validate_passwd(self, passwd):
        return self.get_salted_passwd_hash(passwd) == self.passwd_hash

    @property
    def displayname(self):
        return self.nickname if self.nickname else 'Unnamed User %i' % self.id

    # Allows to manually set the language object for the Usr
    language_obj = relationship(Language)

    # Returns the name of the language of this Usr
    @property
    def language(self):
        return self.language_obj.name if self.language_obj is not None else ''

    # Sets the language object for the Usr from a string
    @language.setter
    def language(self, language_str):
        self.language_obj = \
            get_or_create_language(self, language_str) if language_str else None


class TexHeader(DefaultTableMixin, Base):
    name = Column(Text, nullable=False)
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    creator = relationship(Usr, backref='tex_headers')
    content = Column(Text, nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<TexHeader id=%i name=%s>" % (self.id, self.name)


class Txt(Versioned, DefaultTableMixin, Base):
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    creator = relationship(Usr, backref='txts')

    creation_timestamp = Column(DateTime, nullable=False, default=func.now())
    title = Column(Text, nullable=False)
    authors = Column(Text, nullable=False)
    edition = Column(Text, nullable=False)
    language_id = Column(Integer, ForeignKey(Language.id), nullable=False)
    isbn = Column(Text, nullable=True)  # TODO: ISBN Constraint hinzufügen
    url = Column(Text, nullable=True)

    # Allows to manually set the language object for the txt
    language_obj = relationship(Language)

    # Returns the name of the language of this txt
    @property
    def language(self):
        return self.language_obj.name

    # Sets the language object for the txt from a string
    @language.setter
    def language(self, strlan):
        self.language_obj = get_or_create_language(self, strlan)

    @property
    def displayname(self):
        return '%s (%s)' % (self.title, self.authors)

    def __repr__(self):
        return '<Txt id=%s,displayname="%s">' % (self.id, self.displayname)


class Annotation(Versioned, DefaultTableMixin, Base, TexHeadered):
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    creator = relationship(Usr, backref='annotations')
    creation_timestamp = Column(DateTime, nullable=False, default=func.now())

    written_in_language_id = Column(Integer, ForeignKey(Language.id), nullable=True)
    # Allows to manually set the language object for the Annotation
    language_obj = relationship(Language)

    tex_header_id = Column(Integer, ForeignKey(TexHeader.id), nullable=True)
    tex_header = relationship(TexHeader, backref='annotations')

    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    location = Column(Text, nullable=True)
    txt_id = Column(Integer, ForeignKey(Txt.id), nullable=False)
    txt = relationship(Txt, backref='annotations')

    # Returns the name of the language of this Annotation
    @property
    def language(self):
        return self.language_obj.name

    # Sets the language object for the Annotation from a string
    @language.setter
    def language(self, strlan):
        self.language_obj = get_or_create_language(self, strlan)

    def __repr__(self):
        return '<Annotation id=%s,location="%s",content="%s">' % \
               (self.id, self.location, self.content[0:100])

    @property
    def html_content(self):
        return self.get_with_tex_header(self.content)

    def __json__(self, request):
        return {
            'id': self.id,
            'html_content': self.html_content,
            'title': self.title,
            'content': self.content,
            'location': self.location
        }
