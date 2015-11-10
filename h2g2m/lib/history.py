import urlparse, urllib
import random
from datetime import datetime
from pyramid.events import BeforeRender, subscriber
from pyramid.request import Request as OldRequest
from ..models import DBSession
from sqlalchemy.exc import InvalidRequestError


class Request(OldRequest):
    def route_url(self, route_name, *elements, **kw):
        if not _ignore_for_history(self.environ['PATH_INFO']):
            qs = kw.get('_query', {})
            _init_history(self.session)
            qs['hid'] = str(self.session['history'].current_id)
            kw['_query'] = qs
        return self.route_url_without_hid(route_name, *elements, **kw)

    def route_url_without_hid(self, route_name, *elements, **kw):
        return super(Request, self).route_url(route_name, *elements, **kw)


def is_backworthy(wrapped):
    def append_is_backworthy(*args):
        ret = wrapped(*args)
        ret['is_backworthy'] = True
        return ret

    return append_is_backworthy


class History:
    nodes = []
    current_id = None

    def get_by_id(self, id):
        if not id: return None
        for node in self.nodes:
            if node.id and int(node.id) == int(id): return node
        return None

    def _get_node_repr_in_tree(self, node, depth=1):
        s = (' ' * depth) + str(node) + '\n'
        for child in node.children:
            s += self._get_node_repr_in_tree(child, depth + 1)
        return s

    def __repr__(self):
        s = '<History nodes=%i>\n' % len(self.nodes)
        for node in [n for n in self.nodes if n.parent is None]:
            s += self._get_node_repr_in_tree(node)
        return s.strip()

    def get_last_id(self, request):
        if 'hid' in request.GET:
            try:
                hid = int(request.GET['hid'])
            except ValueError:
                return 0
        else:
            return 0
        if not self.get_by_id(hid): hid = 0
        return hid

    def get_last_backworthy_node(self, request):
        node = self.get_by_id(self.get_last_id(request))
        if not node: return None
        while node:
            if node.is_backworthy and node.db_exists: return node
            node = node.parent
        return node


class HistoryNode:
    forest = None
    id = None
    url = None
    context = None
    parent = None
    is_backworthy = None
    last_visited_ts = None

    @property
    def children(self):
        ret = []
        for node in self.forest.nodes:
            if node.parent and node.parent.id == self.id: ret.append(node)
        return ret

    @property
    def db_exists(self):
        try:
            if DBSession.query(self.context.__class__) \
                    .filter_by(id=self.context.id).count() == 0:
                return False
        except InvalidRequestError, e:
            pass
        return True

    def __init__(self, request, is_backworthy):
        self.forest = request.session['history']
        self.forest.current_id = random.randint(0, 20000000)  # TODO gut so?
        self.id = self.forest.current_id
        self.context = request.context
        self.url = request.current_route_path()
        self.parent = self.forest.get_by_id(self.forest.get_last_id(request))
        self.is_backworthy = is_backworthy
        self.ping()
        self.forest.nodes.append(self)

    def ping(self):
        self.last_visited_ts = datetime.now()

    def __repr__(self):
        return '<HistoryNode id=%i url=%s%s>' % (self.id, self.url, ' *' if self.is_backworthy else '')


def _ignore_for_history(url):
    return [i for i in ['less', 'static', '_debug_toolbar'] if url.startswith('/%s' % i)]


def _init_history(session):
    if 'history' not in session:
        session['history'] = History()
        session.save()


@subscriber(BeforeRender)
def history_recorder(event):
    request = event['request']
    if not request: return
    if (event['view'] is None): return
    if _ignore_for_history(request.environ['PATH_INFO']): return

    is_backworthy = \
        'is_backworthy' in event.rendering_val \
        and event.rendering_val['is_backworthy']
    _init_history(request.session)
    HistoryNode(request, is_backworthy)
    # TODO http://stackoverflow.com/questions/15029173
    # print request.session['history']


def get_back_link(request):
    _init_history(request.session)
    node = request.session['history'].get_last_backworthy_node(request)
    if not node: return '/'

    url = list(urlparse.urlparse(node.url))
    if node.parent:
        d = urlparse.parse_qs(url[4])
        d['hid'] = node.parent.id
        url[4] = urllib.urlencode(d)
    return urlparse.urlunparse(url)
