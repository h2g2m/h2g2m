# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

import webhelpers.html.tags as t
from webhelpers.html.tags import * 
from webhelpers.html.tools import * 

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from h2g2m.models import Txt

from sqlalchemy import or_, and_

import time, re
from collections import Iterable
import hashlib, random

from pyramid.renderers import render

from textextmode import h2g2mTeX, h2g2mTeXScanner
from yapps import runtime
    
from pyramid.security import (
    remember, 
    forget,
    authenticated_userid, 
    unauthenticated_userid,
    has_permission,
    Allowed,
    Denied
)

from pyramid.threadlocal import get_current_registry

def int_as_eur(i):
    return (u'%.2f €' % (i/100.)).replace('.', ',')
    
def today():
    return time.strftime('%Y-%m-%d', time.localtime())

def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def is_loggedin(request):
    return authenticated_userid(request) is not None

def is_admin(request):
    return bool(has_permission('administrate',request.context,request))

def is_myself(usr,request):
    return request.usr.id == usr.id if is_loggedin(request) else False
    
def hiddenfield(form, id, **kwargs):
    return Literal(form.hidden(id, **kwargs) + form.errorlist(id, class_='help-inline'))


def formfield(form, id, caption, fieldtype, columns=(3,9), **kwargs):
    field = form.__getattribute__(fieldtype)(id, **kwargs)
    return Literal(render('../templates/formfield.pt', {
        'form' : form,
        'ffm_id' : id,
        'ffm_caption' : caption,
        'ffm_field' : field,
        'ffm_cols': columns }))

def sendmail(request, **kwargs):
    mailer = get_mailer(request)
    message = Message(**kwargs)
    mailer.send(message)

def get_config_string(key):
    return get_current_registry().settings.get(key)

# to convert Dicts to Objects
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

# for template engine
#class Literal(object):
#    def __init__(self, s):
#        self.s =s
#    def __html__(self):
#        return self.s
Literal = t.literal
    
def is_iterable(x):
    return isinstance(x,Iterable)

def parse_textmode_tex(text):
    ret = text
    P = h2g2mTeX(h2g2mTeXScanner(text))
    try:
        ret = P.tex()
    except runtime.SyntaxError, e:
        pass
        #print_error(e, parser._scanner)
    #ret = runtime.wrap_error_reporter(P, 'tex')
    return ret

def extract_and_replace_mathmodes(s):
    if not s: return s
    mathmode_delims = [
        (ur'\[', ur'\]'),
        (ur'$$', ur'$$'),
        (ur'$', ur'$'),
        (ur'\begin{align}', ur'\end{align}'),
        (ur'\begin{align*}', ur'\end{align*}'),
    ] # TODO (Lars): in der MathJax-Docu nachsehen, ob evtl. noch mehr erlaubt sind
    r = ''
    reps = []
    i = 0
    while i < len(s):
        for delims in mathmode_delims:
            if s[i:].startswith(delims[0]):
                
                t = s[i:i+len(delims[0])]
                i += len(delims[0])
                while i < len(s) and not s[i:].startswith(delims[1]):
                    t += s[i]
                    i += 1
                t += s[i:i+len(delims[1])]
                
                hash = None
                if (not hash) or (hash in s):
                    m = hashlib.sha256()
                    m.update(t)
                    m.update(str(random.getrandbits(16)))
                    hash = m.hexdigest()
                i += len(delims[1])
                reps.append((hash, t))
                r += hash
                break
        if i<len(s): r += s[i]
        i += 1
    return r, reps

def resubst_mathmodes(s, reps):
    if not s: return s
    for a, b in reps:
        s = s.replace(a, b)
    return s

def do_latex(s):
    if not s: return s
    s, reps = extract_and_replace_mathmodes(s)
    parsed = parse_textmode_tex(s)
    if parsed: s = parsed
    s = resubst_mathmodes(s, reps)
    if not s: return ''
    return s
    
    # TODO (Jesko): Wollen wir das benutzen? Load auf dem Server versus load beim client.
    return Literal(re.sub(r"([^\\])\$(([^\$\\]|\\.)*)\$", 
        lambda m: '%s<script type="math/tex">%s</script>'%m.groups()[:2], s))

def get_default_tex_header_id(request):
    l = [ 
        tex_header.id 
        for tex_header 
        in request.usr.tex_headers 
        if tex_header.is_default 
    ]
    return l[0] if l else None

if __name__ == '__main__':

    #parse_textmode_tex('Test')
    
    tests = [
        ur'Test $a=b$ Test', 
        ur'Test $\sqrt{a}$ Test', 
        ur'Test $$\sqrt{a}$$ Test', 
        ur'Test \[\sqrt{a}\] Test', 
        ur'Test \begin{align}\sqrt{a}\end{align} Test', 
        ur'''Test \begin{align}
    \sqrt{a}
    \end{align} Test''', 
        ur'''Test \begin{align*}
    a=b
    \end{align*} Test $x^3+54\sqrt{x+5}$''', 
    ]
    for s in tests:
        t, reps = extract_and_replace_mathmodes(s)
        if '$' in t or ur'\[' in t or ur'\]' in t: 
            print 'ERROR 1 in'
            print s, t, reps
            exit()
        else: print '.', 
        if resubst_mathmodes(t, reps) == s: print '.', 
        else:
            print 'ERROR 2 in '
            print s, t, reps
            exit()