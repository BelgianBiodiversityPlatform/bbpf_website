# -*- coding: utf-8 -*-

import logging

from sqlalchemy import sql

from amnesia.widgets import Widget
from amnesia.utils.widgets import widget_config
from amnesia.modules.folder import Folder
from amnesia.modules.document import Document
from amnesia.modules.file import File

log = logging.getLogger(__name__)


def includeme(config):
    config.scan(__name__)


@widget_config('twitter')
class Twitter(Widget):

    template = 'amnesiabbpf:templates/widgets/twitter.pt'

    def __init__(self, request, embed):
        super().__init__(request)
        self.embed = embed


@widget_config('box_row')
class BoxRow(Widget):

    template = 'amnesiabbpf:templates/widgets/box_row.pt'

    def __init__(self, request, root_id):
        super().__init__(request)
        self.root_id = root_id
        self.folder = self.dbsession.query(Folder).enable_eagerloads(False).\
            get(root_id)

        if self.folder:
            self.documents = self.dbsession.query(Document).filter(
                Document.filter_published(),
                Document.filter_container_id(root_id)
            ).order_by(Document.weight.desc()).all()
        else:
            self.documents = []


@widget_config('slider1')
class Slider1(Widget):

    template = 'amnesiabbpf:templates/widgets/slider1.pt'

    def __init__(self, request, root_id):
        super().__init__(request)
        self.root_id = root_id
        self.folder = self.dbsession.query(Folder).enable_eagerloads(False).\
            get(root_id)

        if self.folder:
            self.files = self.dbsession.query(File).filter(
                File.filter_published(),
                File.filter_container_id(root_id)
            ).order_by(File.weight.desc()).all()
        else:
            self.files = []


@widget_config('slider2')
class Slider2(Widget):

    template = 'amnesiabbpf:templates/widgets/slider2.pt'

    def __init__(self, request, root_id):
        super().__init__(request)
        self.root_id = root_id
        self.folder = self.dbsession.query(Folder).enable_eagerloads(False).\
            get(root_id)

        if self.folder:
            self.documents = self.dbsession.query(Document).filter(
                Document.filter_published(),
                Document.filter_container_id(root_id)
            ).order_by(sql.func.random()).all()
        else:
            self.documents = []
