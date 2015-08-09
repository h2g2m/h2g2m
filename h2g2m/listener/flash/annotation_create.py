from h2g2m.lib.bus.listener_base import Listener


class FlashAnnotationCreatedListener(Listener):
    def __call__(self, event):
        ':type event: AnnotationCreatedEvent'
        event.request.session.flash(('success', u'Annotation successfully created.'))

