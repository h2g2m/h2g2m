# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import declared_attr
from pyramid.renderers import render
import webhelpers.html.tags as t
import helpers as h
from base import DBSession


class NameMixin(object):
    @declared_attr
    def __tablename__(cls):
        return h.camelcase_to_underscore(cls.__name__)


class ComparableMixin(object):
    @property
    def UID(self):
        t = tuple(self.__dict__[column.name] for column in class_mapper(self.__class__).primary_key)
        return t if len(t) > 1 else t[0]

    def __hash__(self):
        return hash(self.UID)

    def __eq__(self, other):
        return self.UID == other.UID


class IdMixin(object):
    id = Column(Integer, primary_key=True)


class DefaultTableMixin(NameMixin, IdMixin, ComparableMixin):
    pass


class TexHeadered:
    def get_with_tex_header(self, content):
        return t.literal(render('../templates/latex.pt', {
            'tex_header': self.tex_header,
            'content': content,
        }))
