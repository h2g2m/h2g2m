from h2g2m.lib.bus.listener_base import Listener


class FlashAnnotationDeletedListener(Listener):
    def __call__(self, event):
        ':type event: AnnotationDeletedEvent'
        event.request.session.flash(('success', u'Annotation successfully deleted.'))
