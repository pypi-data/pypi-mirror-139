from steamship.data.file import FileImportRequest, FileImportResponse
from steamship.plugin.service import PluginRequest, PluginResponse

__copyright__ = "Steamship"
__license__ = "MIT"

from ..demo_apps.plugin_file_importer import TestFileImporterPlugin, TEST_DOC

TEST_REQ = FileImportRequest(
    value="Hi there."
)
TEST_PLUGIN_REQ = PluginRequest(data=TEST_REQ)
TEST_REQ_DICT = TEST_PLUGIN_REQ.to_dict()


def _test_resp(res):
    assert (type(res) == PluginResponse)
    assert (type(res.data) == FileImportResponse)
    assert (res.data.data == TEST_DOC)


def test_importer():
    importer = TestFileImporterPlugin()
    res = importer.run(TEST_PLUGIN_REQ)
    _test_resp(res)
