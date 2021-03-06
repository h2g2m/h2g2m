# !!! do not edit this file manually since it will be overwritte by a call of generate-yapps2-parser.sh in the root directory of the project. This is a parser generated by yapps2 and the h2g2mTex.g file in the parser directory

from pyramid.request import Request
from pyramid.threadlocal import get_current_registry
try:
    from .. import config
except:
    pass

import webhelpers.html.tags as t
Literal = t.literal

def br():
    return Literal(u'<br />')
def em(x):
    return Literal(u'<em>') + x + Literal(u'</em>')
def it(x):
    return Literal(u'<i>') + x + Literal(u'</i>')
def bf(x):
    return Literal(u'<b>') + x + Literal(u'</b>')

def img(x):
    return Literal(u'<img src="%s" style="max-width:600px;" />' % x)
    
def url(x):
    return href(x,x)
def ref(id):
    id = int(id)
    request = Request.blank('/')
    try:
        request.registry = get_current_registry()
        url = request.route_path('annotation.view', annotation_id=id)
    except:
        url = '/404'
    return Literal(u'<a href="%s">Annotation %i</a>' % (url, id))
 
def href(x, y):
    if not x.startswith('http://') and not x.startswith('https://'): x = 'http://'+x
    if y.startswith('http://'): y = y[7:]
    if y.startswith('https://'): y = y[8:]
    return Literal(u'<a href="' + x + '" target="blank">')+ y + Literal(u'</a>')
def ul(x):
    return Literal(u'<ul>') + x + Literal(u'</ul>')
def ol(x):
    return Literal(u'<ol>') + x + Literal(u'</ol>')
def dl(x):
    return Literal(u'<dl class="dl-horizontal">') + x + Literal(u'</dl>')
def li(x):
    return Literal(u'<li>') + x + Literal(u'</li>')
def dt(x):
    return Literal(u'<dt>') + x + Literal(u'</dt>')
def dd(x):
    return Literal(u'<dd>') + x + Literal(u'</dd>')


# Begin -- grammar generated by Yapps
import sys, re
from yapps import runtime

class h2g2mTeXScanner(runtime.Scanner):
    patterns = [
        ("''", re.compile('')),
        ("'\\]'", re.compile('\\]')),
        ("'\\['", re.compile('\\[')),
        ("'description'", re.compile('description')),
        ("'enumerate'", re.compile('enumerate')),
        ("'itemize'", re.compile('itemize')),
        ("r'\\b'", re.compile('\\b')),
        ('EOF', re.compile('$')),
        ('EMPTY', re.compile('')),
        ('BS', re.compile('\\\\')),
        ('NEWLINE', re.compile('\\\\\\\\')),
        ('PARAGRAPH', re.compile('(\\r?\\n\\r?){2}')),
        ('BEGIN', re.compile('\\\\begin\\b')),
        ('END', re.compile('\\\\end\\b')),
        ('ITEM', re.compile('\\\\item\\b')),
        ('EMPH', re.compile('\\\\emph\\b')),
        ('URL', re.compile('\\\\url\\b')),
        ('IMG', re.compile('\\\\img\\b')),
        ('HREF', re.compile('\\\\href\\b')),
        ('REF', re.compile('\\\\ref\\b')),
        ('ITALIC', re.compile('\\\\textit\\b')),
        ('BOLD', re.compile('\\\\textbf\\b')),
        ('WHITESPACE', re.compile('\\s')),
        ('NONWHITESPACE', re.compile('\\S')),
        ('RESERVED', re.compile('[#%^&{}\\\\]')),
        ('NUMBER', re.compile('\\d+')),
        ('CHAR', re.compile('[^#%^&{}\\\\ ]')),
        ('CHAROPITEM', re.compile('[^#%^&{}\\\\\\] ]')),
        ('OB', re.compile('{')),
        ('CB', re.compile('}')),
        ('WORD', re.compile('\\w+')),
        ('SPACE', re.compile('\\\\ ')),
        ('PLAINBS', re.compile('\\\\textbackslash')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{},str,*args,**kw)

class h2g2mTeX(runtime.Parser):
    Context = runtime.Context
    def group(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'group', [])
        OB = self._scan('OB', context=_context)
        text = self.text(_context)
        CB = self._scan('CB', context=_context)
        return text

    def number_group(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'number_group', [])
        OB = self._scan('OB', context=_context)
        number = self.number(_context)
        CB = self._scan('CB', context=_context)
        return number

    def number(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'number', [])
        _token = self._peek('NUMBER', 'OB', context=_context)
        if _token == 'NUMBER':
            NUMBER = self._scan('NUMBER', context=_context)
            return NUMBER
        else: # == 'OB'
            number_group = self.number_group(_context)
            return number_group

    def atom(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'atom', [])
        _token = self._peek('CHAR', 'OB', context=_context)
        if _token == 'CHAR':
            CHAR = self._scan('CHAR', context=_context)
            return CHAR
        else: # == 'OB'
            group = self.group(_context)
            return group

    def href(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'href', [])
        x = ''
        y = ''
        HREF = self._scan('HREF', context=_context)
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        x += atom
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        y += atom
        return href(x,y)

    def url(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'url', [])
        URL = self._scan('URL', context=_context)
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        return url(atom)

    def img(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'img', [])
        IMG = self._scan('IMG', context=_context)
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        return img(atom)

    def ref(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'ref', [])
        REF = self._scan('REF', context=_context)
        while self._peek('NUMBER', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        number = self.number(_context)
        return ref(number)

    def emph(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'emph', [])
        EMPH = self._scan('EMPH', context=_context)
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        return em(atom)

    def textit(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'textit', [])
        ITALIC = self._scan('ITALIC', context=_context)
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        return it(atom)

    def textbf(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'textbf', [])
        BOLD = self._scan('BOLD', context=_context)
        while self._peek('CHAR', 'OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        atom = self.atom(_context)
        return bf(atom)

    def plainbs(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'plainbs', [])
        PLAINBS = self._scan('PLAINBS', context=_context)
        _token = self._peek('OB', "r'\\b'", context=_context)
        if _token == 'OB':
            OB = self._scan('OB', context=_context)
            CB = self._scan('CB', context=_context)
        else: # == "r'\\b'"
            self._scan("r'\\b'", context=_context)
        return '\\'

    def char(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'char', [])
        _token = self._peek('CHAR', 'PLAINBS', context=_context)
        if _token == 'CHAR':
            CHAR = self._scan('CHAR', context=_context)
            return CHAR
        else: # == 'PLAINBS'
            plainbs = self.plainbs(_context)
            return plainbs

    def charopitem(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'charopitem', [])
        _token = self._peek('CHAROPITEM', 'PLAINBS', context=_context)
        if _token == 'CHAROPITEM':
            CHAROPITEM = self._scan('CHAROPITEM', context=_context)
            return CHAROPITEM
        else: # == 'PLAINBS'
            plainbs = self.plainbs(_context)
            return plainbs

    def textspace(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'textspace', [])
        sp = ''
        while 1:
            while 1:
                _token = self._peek('WHITESPACE', 'SPACE', context=_context)
                if _token == 'WHITESPACE':
                    WHITESPACE = self._scan('WHITESPACE', context=_context)
                else: # == 'SPACE'
                    SPACE = self._scan('SPACE', context=_context)
                if self._peek('WHITESPACE', 'SPACE', 'PARAGRAPH', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', 'CHAR', 'PLAINBS', 'CHAROPITEM', 'CB', "'\\]'", 'BEGIN', 'EOF', 'END', 'ITEM', context=_context) not in ['WHITESPACE', 'SPACE']: break
            sp += ' '
            if self._peek('WHITESPACE', 'SPACE', 'PARAGRAPH', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', 'CHAR', 'PLAINBS', 'CHAROPITEM', 'CB', "'\\]'", 'BEGIN', 'EOF', 'END', 'ITEM', context=_context) not in ['WHITESPACE', 'SPACE']: break
        return sp

    def newline(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'newline', [])
        NEWLINE = self._scan('NEWLINE', context=_context)
        return br()

    def paragraph(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'paragraph', [])
        PARAGRAPH = self._scan('PARAGRAPH', context=_context)
        return br()*2

    def chunk(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'chunk', [])
        result = ''
        while 1:
            char = self.char(_context)
            result += char
            if self._peek('CHAR', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', 'CB', 'BEGIN', 'EOF', 'END', 'ITEM', context=_context) not in ['CHAR', 'PLAINBS']: break
        return result

    def chunkopitem(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'chunkopitem', [])
        result = ''
        while 1:
            charopitem = self.charopitem(_context)
            result += charopitem
            if self._peek('CHAROPITEM', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', "'\\]'", context=_context) not in ['CHAROPITEM', 'PLAINBS']: break
        return result

    def format(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'format', [])
        result = ''
        while 1:
            _token = self._peek('PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', context=_context)
            if _token == 'PARAGRAPH':
                paragraph = self.paragraph(_context)
                result += paragraph
            elif _token in ['WHITESPACE', 'SPACE']:
                textspace = self.textspace(_context)
                result += textspace
            elif _token == 'EMPH':
                emph = self.emph(_context)
                result += emph
            elif _token == 'URL':
                url = self.url(_context)
                result += url
            elif _token == 'IMG':
                img = self.img(_context)
                result += img
            elif _token == 'HREF':
                href = self.href(_context)
                result += href
            elif _token == 'REF':
                ref = self.ref(_context)
                result += ref
            elif _token == 'ITALIC':
                textit = self.textit(_context)
                result += textit
            elif _token == 'BOLD':
                textbf = self.textbf(_context)
                result += textbf
            else: # == 'NEWLINE'
                newline = self.newline(_context)
                result += newline
            if self._peek('PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', 'CHAR', 'PLAINBS', 'CHAROPITEM', 'CB', "'\\]'", 'BEGIN', 'EOF', 'END', 'ITEM', context=_context) not in ['PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE']: break
        return result

    def text(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'text', [])
        result = ''
        while 1:
            _token = self._peek('CHAR', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', context=_context)
            if _token in ['CHAR', 'PLAINBS']:
                chunk = self.chunk(_context)
                result += chunk
            else:
                format = self.format(_context)
                result += format
            if self._peek('CHAR', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', 'CB', 'BEGIN', 'EOF', 'END', 'ITEM', context=_context) not in ['CHAR', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE']: break
        return result

    def textopitem(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'textopitem', [])
        result = ''
        while 1:
            _token = self._peek('CHAROPITEM', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', context=_context)
            if _token in ['CHAROPITEM', 'PLAINBS']:
                chunkopitem = self.chunkopitem(_context)
                result += chunkopitem
            else:
                format = self.format(_context)
                result += format
            if self._peek('CHAROPITEM', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', "'\\]'", context=_context) not in ['CHAROPITEM', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE']: break
        return result

    def environment(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'environment', [])
        result = ''
        BEGIN = self._scan('BEGIN', context=_context)
        while self._peek('OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        OB = self._scan('OB', context=_context)
        _token = self._peek("'itemize'", "'enumerate'", "'description'", context=_context)
        if _token == "'itemize'":
            content = ''
            self._scan("'itemize'", context=_context)
            CB = self._scan('CB', context=_context)
            while self._peek('WHITESPACE', 'END', 'ITEM', context=_context) == 'WHITESPACE':
                WHITESPACE = self._scan('WHITESPACE', context=_context)
            while self._peek('END', 'ITEM', context=_context) == 'ITEM':
                item = self.item(_context)
                content += item
            END = self._scan('END', context=_context)
            while self._peek('OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
                WHITESPACE = self._scan('WHITESPACE', context=_context)
            OB = self._scan('OB', context=_context)
            self._scan("'itemize'", context=_context)
            result += ul(content)
        elif _token == "'enumerate'":
            content = ''
            self._scan("'enumerate'", context=_context)
            CB = self._scan('CB', context=_context)
            while self._peek('WHITESPACE', 'END', 'ITEM', context=_context) == 'WHITESPACE':
                WHITESPACE = self._scan('WHITESPACE', context=_context)
            while self._peek('END', 'ITEM', context=_context) == 'ITEM':
                item = self.item(_context)
                content += item
            END = self._scan('END', context=_context)
            while self._peek('OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
                WHITESPACE = self._scan('WHITESPACE', context=_context)
            OB = self._scan('OB', context=_context)
            self._scan("'enumerate'", context=_context)
            result += ol(content)
        else: # == "'description'"
            content = ''
            self._scan("'description'", context=_context)
            CB = self._scan('CB', context=_context)
            while self._peek('WHITESPACE', 'END', 'ITEM', context=_context) == 'WHITESPACE':
                WHITESPACE = self._scan('WHITESPACE', context=_context)
            while self._peek('END', 'ITEM', context=_context) == 'ITEM':
                opitem = self.opitem(_context)
                content += opitem
            END = self._scan('END', context=_context)
            while self._peek('OB', 'WHITESPACE', context=_context) == 'WHITESPACE':
                WHITESPACE = self._scan('WHITESPACE', context=_context)
            OB = self._scan('OB', context=_context)
            self._scan("'description'", context=_context)
            result += dl(content)
        CB = self._scan('CB', context=_context)
        return result

    def item(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'item', [])
        ITEM = self._scan('ITEM', context=_context)
        inline_tex = self.inline_tex(_context)
        return li(inline_tex)

    def opitem(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'opitem', [])
        content = ''
        ITEM = self._scan('ITEM', context=_context)
        while self._peek("'\\['", "''", 'WHITESPACE', context=_context) == 'WHITESPACE':
            WHITESPACE = self._scan('WHITESPACE', context=_context)
        _token = self._peek("'\\['", "''", context=_context)
        if _token == "'\\['":
            self._scan("'\\['", context=_context)
            textopitem = self.textopitem(_context)
            self._scan("'\\]'", context=_context)
            content += dt(textopitem)
        else: # == "''"
            self._scan("''", context=_context)
        inline_tex = self.inline_tex(_context)
        content += dd(inline_tex)
        return content

    def inline_tex(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'inline_tex', [])
        result = ''
        while self._peek('BEGIN', 'CHAR', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', 'EOF', 'END', 'ITEM', context=_context) not in ['EOF', 'END', 'ITEM']:
            _token = self._peek('BEGIN', 'CHAR', 'PLAINBS', 'PARAGRAPH', 'WHITESPACE', 'SPACE', 'EMPH', 'URL', 'IMG', 'HREF', 'REF', 'ITALIC', 'BOLD', 'NEWLINE', context=_context)
            if _token == 'BEGIN':
                environment = self.environment(_context)
                result += environment
            else:
                text = self.text(_context)
                result += text
        return result

    def tex(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'tex', [])
        inline_tex = self.inline_tex(_context)
        EOF = self._scan('EOF', context=_context)
        return inline_tex


def parse(rule, text):
    P = h2g2mTeX(h2g2mTeXScanner(text))
    return runtime.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
