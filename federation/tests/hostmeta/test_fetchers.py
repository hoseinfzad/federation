import json
from unittest.mock import patch

from federation.hostmeta.fetchers import (
    fetch_nodeinfo_document, fetch_nodeinfo2_document, fetch_statisticsjson_document)


class TestFetchNodeInfoDocument:
    dummy_doc = json.dumps({"links": [
        {"href": "https://example.com/1.0", "rel": "http://nodeinfo.diaspora.software/ns/schema/1.0"},
        {"href": "https://example.com/2.0", "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0"},
        {"href": "https://example.com/3.0", "rel": "http://nodeinfo.diaspora.software/ns/schema/3.0"},
    ]})

    @patch("federation.hostmeta.fetchers.fetch_document", return_value=(dummy_doc, 200, None), autospec=True)
    @patch("federation.hostmeta.fetchers.parse_nodeinfo_document", autospec=True)
    def test_makes_right_calls(self, mock_parse, mock_fetch):
        fetch_nodeinfo_document('example.com')
        args, kwargs = mock_fetch.call_args_list[0]
        assert kwargs['host'] == 'example.com'
        assert kwargs['path'] == '/.well-known/nodeinfo'
        args, kwargs = mock_fetch.call_args_list[1]
        assert kwargs['url'] == 'https://example.com/2.0'
        mock_parse.assert_called_once_with(json.loads(self.dummy_doc), 'example.com')


class TestFetchNodeInfo2Document:
    @patch("federation.hostmeta.fetchers.fetch_document", return_value=('{"foo": "bar"}', 200, None), autospec=True)
    @patch("federation.hostmeta.fetchers.parse_nodeinfo2_document", autospec=True)
    def test_makes_right_calls(self, mock_parse, mock_fetch):
        fetch_nodeinfo2_document('example.com')
        args, kwargs = mock_fetch.call_args
        assert kwargs['host'] == 'example.com'
        assert kwargs['path'] == '/.well-known/x-nodeinfo2'
        mock_parse.assert_called_once_with({"foo": "bar"}, 'example.com')


class TestFetchStatisticsJSONDocument:
    @patch("federation.hostmeta.fetchers.fetch_document", return_value=('{"foo": "bar"}', 200, None), autospec=True)
    @patch("federation.hostmeta.fetchers.parse_statisticsjson_document", autospec=True)
    def test_makes_right_calls(self, mock_parse, mock_fetch):
        fetch_statisticsjson_document('example.com')
        args, kwargs = mock_fetch.call_args
        assert kwargs['host'] == 'example.com'
        assert kwargs['path'] == '/statistics.json'
        mock_parse.assert_called_once_with({"foo": "bar"}, 'example.com')
