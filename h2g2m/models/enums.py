# -*- coding: utf-8 -*-
from sqlalchemy import Enum

permission_enum_type = Enum(u'usr', u'grp', u'world', name='permission_enum')
