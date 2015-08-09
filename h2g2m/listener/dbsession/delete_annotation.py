from h2g2m.lib.bus.listener_base import Listener


class DeleteAnnotationListener(Listener):
    def __call__(self, event):
        ':type event: AnnotationDeletedEvent'
        event.DBSession.delete(event.annotation)


