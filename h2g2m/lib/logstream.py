from h2g2m.models import DBSession, Txt, Annotation
import h2g2m.lib.helpers as h


class LogEntry:
    request = None

    type = None
    person = None
    data = None

    def __init__(self, request, type, person, data):
        self.request = request
        self.type = type
        self.person = person
        self.data = data

    def __repr__(self):
        ret = '[%s] ' % self.data.creation_timestamp
        if self.type == 'add_txt':
            ret += h.Literal('%s added the text %s' % ( \
                self.person.displayname, self.data.displayname))
        elif self.type == 'add_annotation':
            ret += h.Literal('%s added the annotation <a href="%s">%s</a>' % ( \
                self.person.displayname,
                self.request.route_path('annotation.view', annotation_id=self.data.id),
                self.data.title
            ))
        else:
            ret += 'TODO'
        return ret


def get_logstream(request):
    if not request.usr: return []
    n = 10
    txts = DBSession.query(Txt). \
        order_by(Txt.creation_timestamp.desc()). \
        limit(n)
    annotations = DBSession.query(Annotation). \
        order_by(Annotation.creation_timestamp.desc()). \
        limit(n)

    log = []
    for txt in txts:
        log.append(LogEntry(request, 'add_txt', txt.creator, txt))
    for annotation in annotations:
        log.append(LogEntry(request, 'add_annotation', annotation.creator, annotation))
    log.sort(key=lambda x: x.data.creation_timestamp, reverse=True)
    return log[:n]
