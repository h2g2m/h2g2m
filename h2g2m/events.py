from h2g2m.lib.bus.event_base import Event


class TxtCreatedEvent(Event):
    ':type txt: Txt'
    txt = None


class TxtEditedEvent(Event):
    ':type txt: Txt'
    txt = None


class TxtDeletedEvent(Event):
    ':type txt: Txt'
    txt = None


class AnnotationCreatedEvent(Event):
    ':type annotation: Annotation'
    annotation = None


class AnnotationEditedEvent(Event):
    ':type annotation: Annotation'
    annotation = None


class AnnotationDeletedEvent(Event):
    ':type annotation: Annotation'
    annotation = None

