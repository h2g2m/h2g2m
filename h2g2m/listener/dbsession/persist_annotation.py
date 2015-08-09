from h2g2m.lib.bus.listener_base import Listener


class PersistAnnotationListener(Listener):
    def __call__(self, event):
        ':type event: AnnotationCreatedEvent|AnnotationEditedEvent'
        event.DBSession.add(event.annotation)
        event.DBSession.flush()
