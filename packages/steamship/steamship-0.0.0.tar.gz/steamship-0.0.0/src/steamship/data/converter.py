import base64
import logging
from dataclasses import dataclass
from typing import Dict, Any

from steamship import MimeTypes
from steamship.base import Client
from steamship.data.block import Block


@dataclass
class ClientsideConvertRequest:
    type: str = None
    plugin: str = None
    id: str = None
    handle: str = None
    name: str = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "ClientsideConvertRequest":
        return ClientsideConvertRequest(
            type=d.get('type', None),
            plugin=d.get('plugin', None),
            id=d.get('id', None),
            handle=d.get('handle', None),
            name=d.get('name', None)
        )


@dataclass
class ConvertResponse():
    root: Block = None

    @staticmethod
    def from_dict(d: any = None, client: Client = None) -> "ConvertResponse":
        if d is None:
            return None

        return ConvertResponse(
            root=Block.from_dict(d.get('root', None), client=client)
        )

    def to_dict(self) -> Dict:
        if self.root is None:
            return dict()
        return dict(root=self.root.to_dict())


TEXT_MIME_TYPES = [
    MimeTypes.TXT,
    MimeTypes.MKD,
    MimeTypes.HTML,
    MimeTypes.DOCX,
    MimeTypes.PPTX
]


@dataclass
class ConvertRequest:
    plugin: str = None
    data: Any = None
    defaultMimeType: str = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "ConvertRequest":
        logging.info("ConvertRequest.fromDict {} {}".format(type(d), d))
        data = d.get('data', None)
        if data is not None and d.get('isBase64', False):
            data_bytes = base64.b64decode(data)
            if d.get('defaultMimeType', None) in TEXT_MIME_TYPES:
                data = data_bytes.decode('utf-8')
            else:
                data = data_bytes

        return ConvertRequest(
            plugin=d.get('plugin', None),
            data=data,
            defaultMimeType=d.get('defaultMimeType', None)
        )
