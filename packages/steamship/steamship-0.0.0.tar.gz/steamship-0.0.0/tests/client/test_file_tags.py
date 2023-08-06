from steamship import MimeTypes

from .helpers import _random_name, _steamship

__copyright__ = "Steamship"
__license__ = "MIT"


def test_file_tag():
    steamship = _steamship()
    name_a = "{}.mkd".format(_random_name())
    a = steamship.upload(
        name=name_a,
        content="A",
        mimeType=MimeTypes.MKD
    ).data
    assert (a.id is not None)
    assert (a.name == name_a)
    assert (a.mimeType == MimeTypes.MKD)

    a.add_tags(['test1', 'test2'])

    tags = a.list_tags().data.tags
    print(tags)
    assert (len(tags) == 2)

    must = ['test1', 'test2']
    for tag in tags:
        assert (tag.name in must)
        must.remove(tag.name)
    assert (len(must) == 0)

    a.remove_tags(['test1'])

    tags = a.list_tags().data.tags
    print(tags)
    assert (len(tags) == 1)

    must = ['test2']
    for tag in tags:
        assert (tag.name in must)
        must.remove(tag.name)
    assert (len(must) == 0)

    a.remove_tags(['test2'])
    tags = a.list_tags().data.tags
    print(tags)
    assert (len(tags) == 0)

    a.delete()
