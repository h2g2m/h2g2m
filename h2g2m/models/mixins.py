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
        t = tuple( self.__dict__[column.name] for column in class_mapper(self.__class__).primary_key )
        return t if len(t) > 1 else t[0]
    def __hash__(self):
        return hash(self.UID)
    def __eq__(self,other):
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


class TreeedDbObject:

    @property
    def element_count_at_same_level(self):
        return DBSession.query(self.__class__).\
            filter_by(parent_id=self.parent_id).count()

    def prepare_deletion(self):
        # move all categories at parent level by one
        DBSession.query(self.__class__).\
            filter_by(parent_id=self.parent_id).\
            filter(self.__class__.sort_order>self.sort_order).\
            update({'sort_order': self.__class__.sort_order-1})

    @property
    def is_last(self):
        return self.sort_order == self.element_count_at_same_level

    @property
    def is_first(self):
        return self.sort_order == 1

    def has_parent(self):
        return True if self.parent_id else False

    @property
    def get_new_sort_order(self):
        return self.element_count_at_same_level+1

    @property
    def parent(self):
        try:
            return DBSession.query(self.__class__).filter_by(id=self.parent_id).one()
        except NoResultFound:
            return None

    @property
    def children(self):
        return DBSession.query(self.__class__).filter_by(parent_id=self.id).all()

    def move_to_parent(self):

        # get parent id of parent
        parent_id = self.parent.parent_id

        # move all categories at parent level by one
        DBSession.query(self.__class__).\
            filter_by(parent_id=parent_id).\
            filter(self.__class__.sort_order>self.parent.sort_order).\
            update({'sort_order': self.__class__.sort_order+1})

        # adjust current object
        self.sort_order = self.parent.sort_order+1
        self.parent_id = parent_id
        DBSession.add(self)

    def become_child(self):
        future_parent = DBSession.query(self.__class__).filter_by(
            parent_id = self.parent_id,
            sort_order = self.sort_order-1
            ).one()

        # move all categories at parent level by one
        DBSession.query(self.__class__).\
            filter_by(parent_id=self.parent_id).\
            filter(self.__class__.sort_order>self.sort_order).\
            update({'sort_order': self.__class__.sort_order-1})

        self.parent_id = future_parent.id
        self.sort_order = len(future_parent.children)

    def move(self, direction):
        target_item = DBSession.query(self.__class__).filter_by(
            parent_id=self.parent_id,
            sort_order=self.sort_order+direction
        ).one()
        s = target_item.sort_order
        target_item.sort_order = self.sort_order
        self.sort_order = s
        DBSession.add(target_item)
        DBSession.add(self)
