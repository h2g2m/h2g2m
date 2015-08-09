from h2g2m.events import TxtCreatedEvent, TxtEditedEvent, TxtDeletedEvent, AnnotationCreatedEvent, AnnotationEditedEvent, \
    AnnotationDeletedEvent
from h2g2m.listener.dbsession.delete_annotation import DeleteAnnotationListener
from h2g2m.listener.dbsession.delete_txt import DeleteTxtListener
from h2g2m.listener.dbsession.persist_annotation import PersistAnnotationListener
from h2g2m.listener.dbsession.persist_txt import PersistTxtListener
from h2g2m.listener.flash.annotation_create import FlashAnnotationCreatedListener
from h2g2m.listener.flash.annotation_delete import FlashAnnotationDeletedListener
from h2g2m.listener.flash.annotation_edit import FlashAnnotationEditedListener
from h2g2m.listener.flash.txt_create import FlashTxtCreatedListener
from h2g2m.listener.flash.txt_delete import FlashTxtDeletedListener
from h2g2m.listener.flash.txt_edit import FlashTxtEditedListener


def init_bus(bus):
    bus.subscribe(TxtCreatedEvent, FlashTxtCreatedListener())
    bus.subscribe(TxtCreatedEvent, PersistTxtListener())
    bus.subscribe(TxtEditedEvent, FlashTxtEditedListener())
    bus.subscribe(TxtEditedEvent, PersistTxtListener())
    bus.subscribe(TxtDeletedEvent, DeleteTxtListener())
    bus.subscribe(TxtDeletedEvent, FlashTxtDeletedListener())
    bus.subscribe(AnnotationCreatedEvent, FlashAnnotationCreatedListener())
    bus.subscribe(AnnotationCreatedEvent, PersistAnnotationListener())
    bus.subscribe(AnnotationEditedEvent, FlashAnnotationEditedListener())
    bus.subscribe(AnnotationEditedEvent, PersistAnnotationListener())
    bus.subscribe(AnnotationDeletedEvent, DeleteAnnotationListener())
    bus.subscribe(AnnotationDeletedEvent, FlashAnnotationDeletedListener())
    return bus
