# -*- coding: utf-8 -*-
import random
import hashlib
import re
from sqlalchemy.orm import object_session
from sqlalchemy.orm.util import has_identity
from base import DBSession


def is_transient(obj):
    return object_session(obj) is None and not has_identity(obj)


def is_pending(obj):
    return object_session(obj) is not None and not has_identity(obj)


def is_detached(obj):
    return object_session(obj) is None and has_identity(obj)


def is_persistent(obj):
    return object_session(obj) is not None and has_identity(obj)


def get_state(obj):
    if is_transient(obj): return 'transient'
    if is_pending(obj): return 'pending'
    if is_detached(obj): return 'detached'
    if is_persistent(obj): return 'persistent'


def gen_salt():
    return gen_hash(20, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')


def gen_hash(length, space):
    ret = ''
    for i in range(length):
        ret += space[random.randint(0, len(space) - 1)]
    return hashlib.sha256(ret).hexdigest()


def underscore_to_camelcase(value):
    return re.sub('(^|\_)(.)([^_]*)', lambda m: m.group(2).upper() + m.group(3), value)


def camelcase_to_underscore(value):
    return re.sub('([^A-Z])([A-Z])', r'\1_\2', value).lower()
