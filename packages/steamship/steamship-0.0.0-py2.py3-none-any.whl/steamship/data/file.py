import io
import logging
import re
from typing import Union, Tuple, Any, List

from steamship.base import Client, Response, Request
from steamship.base.binary_utils import flexi_create
from steamship.base.request import IdentifierRequest
from steamship.data.block import Block
from steamship.data.converter import ClientsideConvertRequest, ConvertResponse
from steamship.data.embedding_index import EmbeddingIndex
from steamship.data.embedding_index import IndexItem
from steamship.data.parser import DependencyMatcher, PhraseMatcher, TokenMatcher
from steamship.data.parser import ParseRequest, ParseResponse
from steamship.data.plugin import PluginTargetType
from steamship.data.tag import CreateTagRequest, DeleteTagRequest, ListTagsRequest
from steamship.data.tag import TagObjectRequest

from dataclasses import dataclass


class FileUploadType:
    file = "file"
    url = "url"
    value = "value"
    fileImporter = "fileImporter"


_logger = logging.getLogger(__name__)


def parseDquery(query: str) -> List[Tuple[str, str, str]]:
    query = re.sub(' +', ' ', query.strip())
    parts = re.split(r'\s*(?=[@#])', query)
    ret = []

    for s in parts:
        s = s.strip()
        if not s:
            continue

        command = ''
        if s[0] in ['@', '#']:
            command = s[0]
            s = s[1:]

        if command == '':
            ret.append((command, None, s))
            continue

        if '"' not in s and ":" not in s:
            if command == '#':
                ret.append((command, 'contains', s))
            else:
                ret.append((command, s, None))
            continue

        modifier = None
        if ':' in s:
            ss = s.split(':')
            modifier = ss[0]
            s = ss[1]

        content = s
        if '"' in s:
            i = s.index('"')
            content = s[1 + i:-1]
            if modifier is None:
                s = s[:i]
                modifier = s
                if modifier == '':
                    modifier = None

        ret.append((command, modifier, content))
    return ret


@dataclass
class FileClearResponse:
    id: str


@dataclass
class FileTagRequest(Request):
    id: str
    plugin: str = None


@dataclass
class FileTagResponse:
    id: str
    tagResult: ParseResponse

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "FileTagResponse":
        if 'file' in d:
            d = d['file']
        return FileTagResponse(
            id=d.get('id', None),
            tagResult=ParseResponse.from_dict(d.get('tagResult', {}), client=client)
        )


@dataclass
class SpanQuery:
    text: str = None
    label: str = None
    spanType: str = None


@dataclass
class FileQueryRequest(Request):
    fileId: str
    type: str = None
    hasSpans: List[SpanQuery] = None
    text: str = None
    textMode: str = None
    isQuote: bool = None


@dataclass
class FileQueryResponse:
    id: str
    blocks: List[Block]

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "FileQueryResponse":
        return FileQueryResponse(
            id=d.get('id', None),
            blocks=[Block.from_dict(block, client=client) for block in d.get('blocks', None)]
        )


@dataclass
class FileRawRequest(Request):
    id: str


@dataclass
class ListFilesRequest(Request):
    corpusId: str = None


@dataclass
class ListFilesResponse:
    files: List["File"]

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "ListFilesResponse":
        return ListFilesResponse(
            files=[File.from_dict(f, client=client) for f in d.get('files', [])]
        )


@dataclass
class FileImportRequest:
    value: str = None
    data: str = None
    url: str = None
    type: str = None  # FileUploadType: fileImporter | value | url | data

    mimeType: str = None
    corpusId: str = None
    name: str = None

    plugin: str = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "FileImportRequest":
        return FileImportRequest(
            value=d.get('value', None),
            data=d.get('data', None),
            url=d.get('url', None),
            type=d.get('type', None),
            mimeType=d.get('mimeType', None),
            corpusId=d.get('corpusId', None),
            plugin=d.get('plugin', None),
            name=d.get('name', None)
        )

    def to_dict(self) -> dict:
        return dict(
            value=self.value,
            data=self.data,
            url=self.url,
            type=self.type,
            mimeType=self.mimeType,
            corpusId=self.corpusId,
            plugin=self.plugin,
            name=self.name
        )


@dataclass
class FileImportResponse:
    data: Any = None
    mimeType: str = None

    def __init__(
            self,
            data: Any = None,
            string: str = None,
            bytes: io.BytesIO = None,
            json: io.BytesIO = None,
            mimeType: str = None
    ):
        data, mimeType = flexi_create(
            body=data,
            string=string,
            json=json,
            bytes=bytes,
            mimeType=mimeType
        )
        self.data = data
        self.mimeType = mimeType

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "FileImportResponse":
        return FileImportResponse(
            data=d.get('data', None),
            mimeType=d.get('mimeType', None)
        )

    def to_dict(self) -> dict:
        return dict(
            data=self.data,
            mimeType=self.mimeType
        )


@dataclass
class File:
    """A file.
    """
    client: Client = None
    id: str = None
    name: str = None
    handle: str = None
    mimeType: str = None
    spaceId: str = None
    corpusId: str = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "File":
        if 'file' in d:
            d = d['file']
        return File(
            client=client,
            id=d.get('id', None),
            handle=d.get('handle', None),
            name=d.get('name', None),
            mimeType=d.get('mimeType', None),
            corpusId=d.get('corpusId', None),
            spaceId=d.get('spaceId', None)
        )

    def delete(
            self,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None) -> "Response[File]":
        return self.client.post(
            'file/delete',
            IdentifierRequest(id=self.id),
            expect=File,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def clear(
            self,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None) -> Response[FileClearResponse]:
        return self.client.post(
            'file/clear',
            IdentifierRequest(id=self.id),
            expect=FileClearResponse,
            ifdQuery=self,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    @staticmethod
    def upload(
            client: Client,
            filename: str = None,
            name: str = None,
            content: str = None,
            mimeType: str = None,
            corpusId: str = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None
    ) -> "Response[File]":

        if filename is None and name is None and content is None:
            raise Exception("Either filename or name + content must be provided.")

        if filename is not None:
            with open(filename, 'rb') as f:
                content = f.read()
                name = filename

        req = FileImportRequest(
            type=FileUploadType.file,
            corpusId=corpusId,
            name=name,
            mimeType=mimeType
        )

        return client.post(
            'file/create',
            payload=req,
            file=(name, content, "multipart/form-data"),
            expect=File,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    @staticmethod
    def create(
            client: Client,
            filename: str = None,
            name: str = None,
            url: str = None,
            content: str = None,
            plugin: str = None,
            mimeType: str = None,
            corpusId: str = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None
    ) -> "Response[File]":

        if filename is None and name is None and content is None and url is None and plugin is None:
            raise Exception("Either filename, name + content, url, or plugin must be provided.")

        if filename is not None:
            with open(filename, 'rb') as f:
                content = f.read()
                name = filename

        req = FileImportRequest(
            type=FileUploadType.fileImporter if plugin is not None else FileUploadType.file,
            corpusId=corpusId,
            name=name,
            url=url,
            mimeType=mimeType,
            plugin=plugin
        )

        return client.post(
            'file/create',
            payload=req,
            file=(name, content, "multipart/form-data"),
            expect=File,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    @staticmethod
    def list(
            client: Client,
            corpusId: str = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None
    ):
        req = ListFilesRequest(
            corpusId=corpusId
        )
        res = client.post(
            'file/list',
            payload=req,
            expect=ListFilesResponse,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )
        return res

    @staticmethod
    def scrape(
            client: Client,
            url: str,
            name: str = None,
            corpusId: str = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None) -> "File":
        if name is None:
            name = url
        req = FileImportRequest(
            type=FileUploadType.url,
            name=name,
            url=url,
            corpusId=corpusId
        )

        return client.post(
            'file/create',
            payload=req,
            expect=File,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def convert(
            self,
            plugin: str = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None):
        req = ClientsideConvertRequest(
            id=self.id,
            type=PluginTargetType.file,
            plugin=plugin
        )

        return self.client.post(
            'plugin/convert',
            payload=req,
            expect=ConvertResponse,
            asynchronous=True,
            ifdQuery=self,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def parse(
            self,
            plugin: str = None,
            tokenMatchers: List[TokenMatcher] = None,
            phraseMatchers: List[PhraseMatcher] = None,
            dependencyMatchers: List[DependencyMatcher] = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None
    ):
        req = ParseRequest(
            type=PluginTargetType.file,
            id=self.id,
            plugin=plugin,
            tokenMatchers=tokenMatchers,
            phraseMatchers=phraseMatchers,
            dependencyMatchers=dependencyMatchers
        )

        return self.client.post(
            'plugin/parse',
            payload=req,
            expect=ParseResponse,
            asynchronous=True,
            ifdQuery=self,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def tag(
            self,
            plugin: str = None,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None
    ):
        req = FileTagRequest(
            id=self.id,
            plugin=plugin
        )

        return self.client.post(
            'file/tag',
            payload=req,
            expect=FileTagResponse,
            asynchronous=True,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def dquery(
            self,
            dQuery: str,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None):
        blockType = None
        hasSpans = []
        text = None
        isQuote = None
        textMode = None

        for tup in parseDquery(dQuery):
            (cmd, subcmd, content) = tup
            if cmd == '':
                blockType = content
            elif cmd == '#':
                text = content
                textMode = subcmd
            elif cmd == '@':
                hasSpans.append(SpanQuery(label=subcmd, text=content))

        return self.query(
            blockType=blockType,
            hasSpans=hasSpans,
            text=text,
            textMode=textMode,
            isQuote=isQuote,
            pd=True,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def query(
            self,
            blockType: str = None,
            hasSpans: List[SpanQuery] = None,
            text: str = None,
            textMode: str = None,
            isQuote: bool = None,
            pd: bool = False,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None
    ) -> Response[FileQueryResponse]:

        req = FileQueryRequest(
            fileId=self.id,
            type=blockType,
            hasSpans=hasSpans,
            text=text,
            textMode=textMode,
            isQuote=isQuote
        )
        res = self.client.post(
            'file/query',
            payload=req,
            expect=FileQueryResponse,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )
        return res

    def index(
            self,
            plugin: str = None,
            indexName: str = None,
            blockType: str = None,
            indexId: str = None,
            index: "EmbeddingIndex" = None,
            upsert: bool = True,
            reindex: bool = True,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None) -> "EmbeddingIndex":
        # TODO: This should really be done all on the app, but for now we'll do it in the client
        # to facilitate demos.

        if indexId is None and index is not None:
            indexId = index.id

        if indexName is None:
            indexName = "{}-{}".format(self.id, plugin)

        if indexId is None and index is None:
            index = self.client.create_index(
                name=indexName,
                plugin=plugin,
                upsert=True,
                spaceId=spaceId,
                spaceHandle=spaceHandle,
                space=space
            ).data
        elif index is None:
            index = EmbeddingIndex(
                client=self.client,
                indexId=indexId
            )

        # We have an index available to us now. Perform the query.
        blocks = self.query(
            blockType=blockType,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        ).data.blocks

        items = []
        for block in blocks:
            item = IndexItem(
                value=block.text,
                externalId=block.id,
                externalType="block"
            )
            items.append(item)

        insert_task = index.insert_many(
            items,
            reindex=reindex,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

        insert_task.wait()
        return index

    def raw(
            self,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None):
        req = FileRawRequest(
            id=self.id,
        )

        return self.client.post(
            'file/raw',
            payload=req,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space,
            rawResponse=True
        )

    def add_tags(
            self,
            tags=List[Union[str, CreateTagRequest]],
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None):
        tagsNew = []
        for tag in tags:
            if type(tag) == str:
                tagsNew.append(CreateTagRequest(name=tag, upsert=True))
            elif type(tag) == CreateTagRequest:
                tagsNew.append(tag)
            else:
                raise (Exception("Unable to add tag of type: {}".format(type(tag))))

        req = TagObjectRequest(
            tags=tagsNew,
            objectType='file',
            objectId=self.id
        )

        return self.client.post(
            'tag/create',
            payload=req,
            expect=TagObjectRequest,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def remove_tags(
            self,
            tags=List[Union[str, DeleteTagRequest]],
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None):
        tagsNew = []
        for tag in tags:
            if type(tag) == str:
                tagsNew.append(DeleteTagRequest(name=tag))
            elif type(tag) == DeleteTagRequest:
                tagsNew.append(tag)
            else:
                raise (Exception("Unable to remove tag of type: {}".format(type(tag))))

        req = TagObjectRequest(
            tags=tagsNew,
            objectType='file',
            objectId=self.id
        )

        return self.client.post(
            'tag/delete',
            payload=req,
            expect=FileTagResponse,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )

    def list_tags(
            self,
            spaceId: str = None,
            spaceHandle: str = None,
            space: any = None):
        req = ListTagsRequest(
            objectType='file',
            objectId=self.id
        )

        return self.client.post(
            'tag/list',
            payload=req,
            expect=TagObjectRequest,
            spaceId=spaceId,
            spaceHandle=spaceHandle,
            space=space
        )
