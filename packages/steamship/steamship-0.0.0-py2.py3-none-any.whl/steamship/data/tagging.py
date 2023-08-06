import json
from dataclasses import dataclass
from typing import List

from steamship.base import Client, Request
from steamship.data.block import Block


@dataclass
class TagResponse:
    blocks: List[Block] = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "TagResponse":
        blocks = [Block.from_dict(h) for h in (d.get("blocks", []) or [])]
        return TagResponse(
            blocks=blocks
        )


@dataclass
class TagRequest(Request):
    blocks: List[str] = None
    fileId: str = None
    parsedBlocks: List[Block] = None
    plugin: str = None
    metadata: any = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "TagRequest":
        metadata = d.get("metadata", None)
        if metadata is not None:
            try:
                metadata = json.loads(metadata)
            except:
                pass

        parsedBlocks = [Block.from_dict(dd) for dd in (d.get("parsedBlocks", []) or [])]

        return TagRequest(
            blocks=(d.get("blocks", []) or []),
            fileId=d.get('fileId', None),
            parsedBlocks=parsedBlocks,
            plugin=d.get("plugin", None),
            metadata=metadata
        )
