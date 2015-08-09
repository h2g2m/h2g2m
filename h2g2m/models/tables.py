# -*- coding: utf-8 -*-
from abc import abstractmethod

import re
import hashlib
import collections
import helpers

from sqlalchemy import Column, Integer, Boolean, Text, DateTime, func, or_, and_
from sqlalchemy.schema import Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from pyramid.security import authenticated_userid

from h2g2m.lib.dbversioning import Versioned

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean

from base import Base
from h2g2m.models.mixins import NameMixin

from sqlalchemy.schema import (
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint
)

from base import Base, DBSession
from mixins import DefaultTableMixin, TexHeadered, TreeedDbObject
from enums import permission_enum_type
from ..security import *


def get_or_create(obj, cls, name):
    with DBSession.no_autoflush:
        # print 'START', obj, get_state(obj), cls, name
        # is_pend = is_pending(obj)
        #if is_pend: DBSession.expunge(obj)

        try:
            res = DBSession.query(cls).filter_by(name=name).one()
        except NoResultFound:
            res = cls(name=name)
            # DBSession.add(res)
            # DBSession.flush()
        # TODO: hier vielleicht nicht jedem Benutzer erlauben, Sprachen/Tags anzulegen

        # if is_pend: DBSession.add(obj)
        # print 'END', obj, get_state(obj), cls, name
        return res


def get_or_create_language(obj, language_name):
    return get_or_create(obj, Language, language_name)


def get_or_create_tag(obj, tag_name):
    return get_or_create(obj, Tag, tag_name)


def get_or_create_person(obj, person_name):
    return get_or_create(obj, Person, person_name)


txt_has_annotation = Table('txt_has_annotation', Base.metadata,
                           Column('annotation_id', Integer, ForeignKey('annotation.id')),
                           Column('txt_id', Integer, ForeignKey('txt.id'))
)

annotation_has_tag = Table('annotation_has_tag', Base.metadata,
                           Column('annotation_id', Integer, ForeignKey('annotation.id')),
                           Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Language(DefaultTableMixin, Base):
    shortcut = Column(Text, nullable=True)
    name = Column(Text, nullable=False)


grp_has_grp = Table('grp_has_grp', Base.metadata,
                    Column('grp_id', Integer, ForeignKey('grp.id'), primary_key=True),
                    Column('contains_grp_id', Integer, ForeignKey('grp.id'), primary_key=True)
)


class Grp(DefaultTableMixin, Base):
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    delta_in = relationship('Grp',
                            secondary=grp_has_grp,
                            primaryjoin=id == grp_has_grp.c.grp_id,
                            secondaryjoin=id == grp_has_grp.c.contains_grp_id,
                            backref='delta_out'
    )

    # def __hash__(self):
    # return hash(self.id)
    #    def __eq__(self,other_grp):
    #        return self.id == other_grp.id


    # Performs a breadth-first-search along incoming edges and calls the 
    # callback function for each visited group. If the callback returns True,
    # the BFS routine terminates with the return value True. 
    # If the callback never returns True, the return value of BFS is False.
    #
    # TODO: Tobi sagt, dass man in PostgreSQL vielleicht diese Abfrage schon
    # auf Datenbankebene erledigen kann.

    @property
    def principal(self):
        return '%d' % self.id

    def __bfs(self, getlist):
        queue = collections.deque()
        queue.appendleft(self)
        visited = set()
        while queue:
            node = queue.pop()
            yield node
            for neighbour in getlist(node):
                if not neighbour in visited:
                    queue.appendleft(neighbour)
                    visited.add(neighbour)

    @property
    def members(self):
        for n in self.__bfs(lambda g: g.delta_in):
            yield n

    @property
    def groups(self):
        for n in self.__bfs(lambda g: g.delta_out):
            yield n

    def __contains__(self, other_grp):
        for grp in self.members:
            if grp == other_grp: return True
        return False


class Usr(DefaultTableMixin, Base):
    login = Column(Text, nullable=False,
                   unique=True)  # a unique string used only to login, can be replaced by open-id later
    nickname = Column(Text, nullable=False)  # the nickname displayed to other users
    # TODO Constraint that exactly one Grp exists
    wrapper_grp = relationship(Grp)
    grp_id = Column(Integer, ForeignKey(Grp.id), nullable=False)
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
    def principal(self):
        return '%d' % self.grp_id

    @property
    def groups(self):
        class Box:
            def __init__(self, **kw):
                self.__dict__.update(kw)

        for grp in self.wrapper_grp.groups:
            yield Box(name=grp.principal)

            # TODO: remove the following and see if everything still works
            # yield Box(name=self.principal)
            # yield Box(name=PRINCIPAL_USR)
            #if self.id == 1:
            #   yield Box(name=PRINCIPAL_ADMIN)

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

    @property
    def tag_list(self):
        return set(sum([annotation.tag_list for annotation in self.annotations], []))


class Tag(DefaultTableMixin, Base):
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return self.name


class Person(Versioned, DefaultTableMixin, Base):
    name = Column(Text, nullable=False)

    def __repr__(self):
        return '<Person name=%s>' % self.name


is_author_of = Table('is_author_of', Base.metadata,
                     Column('person_id', Integer, ForeignKey('person.id')),
                     Column('txt_id', Integer, ForeignKey('txt.id'))
)


class TexHeader(DefaultTableMixin, Base):
    name = Column(Text, nullable=False)
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    content = Column(Text, nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    # TODO: Constraint einfügen, die pro User nur einen Default-Header erlaubt

    creator = relationship(Usr, backref='tex_headers')

    def __repr__(self):
        return "<TexHeader id=%i name=%s>" % (self.id, self.name)


class Annotation(Versioned, DefaultTableMixin, Base, TexHeadered):
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    creation_timestamp = Column(DateTime, nullable=False, default=func.now())
    written_in_language_id = Column(Integer, ForeignKey(Language.id), nullable=True)
    tex_header_id = Column(Integer, ForeignKey(TexHeader.id), nullable=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    location = Column(Text, nullable=True)

    creator = relationship(Usr, backref='annotations')
    tex_header = relationship(TexHeader, backref='annotations')

    # Allows to manually set the language object for the Annotation
    language_obj = relationship(Language)
    # Returns the name of the language of this Annotation
    @property
    def language(self):
        return self.language_obj.name

    # Sets the language object for the Annotation from a string
    @language.setter
    def language(self, strlan):
        self.language_obj = get_or_create_language(self, strlan)

    #Allows to manually set a list of tag objects for the Annotation
    tag_list = relationship(Tag, secondary=annotation_has_tag, backref='annotations')

    #Creates a comma separated list of the tags of that annotation
    @property
    def tags(self):
        return ', '.join([a.name for a in self.tag_list])

    #Creates a list of Tags from a comma separated list of names; adds non-existing tags to database
    @tags.setter
    def tags(self, strlist):
        self.tag_list[:] = [get_or_create_tag(self, a.strip()) for a \
                            in re.split('[ ,]', strlist) if a.strip()]

    def __repr__(self):
        return '<Annotation id=%s,location="%s",content="%s">' % \
               (self.id, self.location, self.content[0:100])

    @property
    def html_content(self):
        return self.get_with_tex_header(self.content)

    @property
    def resolutions(self):
        return self._resolutions(self.posts)

    def _resolutions(self, posts):
        res = []
        for post in posts:
            if post.is_resolution: res.append(post)
            res += self._resolutions(post.children)
        return res

    def __json__(self, request):
        return {
            'id': self.id,
            'html_content': self.html_content,
            'title': self.title,
            'content': self.content,
            'location': self.location
        }


annotation_has_post = Table('annotation_has_post', Base.metadata,
                            Column('annotation_id', Integer, ForeignKey('annotation.id')),
                            Column('post_id', Integer, ForeignKey('post.id'))
)


class Post(Versioned, DefaultTableMixin, Base, TexHeadered, TreeedDbObject):
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    creation_timestamp = Column(DateTime, nullable=False, default=func.now())
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey('post.id'), nullable=True)
    is_resolution = Column(Boolean, nullable=False)
    tex_header_id = Column(Integer, ForeignKey(TexHeader.id), nullable=True)

    creator = relationship(Usr)
    annotation = relationship(
        Annotation,
        secondary=annotation_has_post,
        single_parent=True,
        uselist=False,
        backref='posts'
    )
    tex_header = relationship(TexHeader, backref='posts')

    @property
    def html_content(self):
        return self.get_with_tex_header(self.content)


class Txt(Versioned, DefaultTableMixin, Base):
    creator_id = Column(Integer, ForeignKey(Usr.id), nullable=False)
    creation_timestamp = Column(DateTime, nullable=False, default=func.now())
    title = Column(Text, nullable=False)
    edition = Column(Text, nullable=False)
    language_id = Column(Integer, ForeignKey(Language.id), nullable=False)
    isbn = Column(Text, nullable=True)  # TODO: ISBN Constraint hinzufügen
    url = Column(Text, nullable=True)

    creator = relationship(Usr, backref='txts')

    annotations = relationship(Annotation,
                               secondary=txt_has_annotation,
                               backref='txts',
                               order_by=Annotation.location
    )

    # Allows to manually set the authors as a list of Person objects
    author_list = relationship(Person, secondary=is_author_of, backref='texts')
    #Creates a comma separated list of the names of all authors
    @property
    def authors(self):
        return ', '.join([a.name for a in self.author_list])
        #Creates a list of persons from a comma separated list of names; adds non-existing persons to database

    @authors.setter
    def authors(self, strlist):
        self.author_list[:] = [get_or_create_person(self, a.strip()) for a in strlist.split(',')]

    # Allows to manually set the language object for the txt
    language_obj = relationship(Language)
    # Returns the name of the language of this txt
    @property
    def language(self):
        return self.language_obj.name

    #Sets the language object for the txt from a string
    @language.setter
    def language(self, strlan):
        self.language_obj = get_or_create_language(self, strlan)

    @property
    def displayname(self):
        return '%s (%s)' % (self.title, self.authors)

    def __repr__(self):
        return '<Txt id=%s,displayname="%s">' % (self.id, self.displayname)
