import json

from unittest import TestCase
from unittest.mock import patch, Mock

from resourcer import Resource, Response


EXPECTED_URL = 'https://example.com/tag/coding'

EXPECTED_PARAMS = {
    'param1': 'value1',
    'param2': 'value2'
}

EXPECTED_HEADERS = {
    'header1': 'value1',
    'header2': 'value2'
}

EXPECTED_DATA = {
    'data1': 'value1',
    'data2': 'value2'
}

class ResourceTests(TestCase):

    def setUp(self):
        self.resource = Resource('https://{domain}/{path1}/{path2}')

        self.resource.domain = 'example.com'
        self.resource.path1 = 'tag'
        self.resource.path2 = 'coding'

        self.resource.param('param1', 'value1')
        self.resource.param('param2', 'value2')

        self.resource.header('header1', 'value1')
        self.resource.header('header2', 'value2')

        self.resource.data('data1', 'value1')
        self.resource.data('data2', 'value2')

    def test_init(self):
        resource = Resource('https://{domain}/{path1}/{path2}')
        self.assertEqual(resource.domain, None)
        self.assertEqual(resource.path1, None)
        self.assertEqual(resource.path2, None)
        with self.assertRaises(AttributeError):
            resource.path3

    def test_is_valid_true(self):
        self.assertTrue(self.resource.is_valid())

    def test_is_valid_false(self):
        self.resource.path2 = None
        self.assertFalse(self.resource.is_valid())

    def test_to_url_valid(self):
        expected = 'https://example.com/tag/coding'
        self.assertEqual(expected, self.resource.to_url())
        
    def test_header(self):
        self.assertDictEqual(EXPECTED_HEADERS, self.resource._headers)

    def test_param(self):
        self.assertDictEqual(EXPECTED_PARAMS, self.resource._params)

    def test_data(self):
        self.assertDictEqual(EXPECTED_DATA, self.resource._data)

    def test_get(self):
        with patch('requests.get') as mocked_get:
            mocked_get.return_value = Mock(status_code=200, text='{"k1": "v1"}')
            response = self.resource.get()
            mocked_get.assert_called_with(url=EXPECTED_URL, params=EXPECTED_PARAMS, headers=EXPECTED_HEADERS)

    def test_delete(self):
        with patch('requests.delete') as mocked_delete:
            mocked_delete.return_value = Mock(status_code=200, text='{"k1": "v1"}')
            response = self.resource.delete()
            mocked_delete.assert_called_with(url=EXPECTED_URL, params=EXPECTED_PARAMS, headers=EXPECTED_HEADERS)
    
    def test_put(self):
        with patch('requests.put') as mocked_put:
            mocked_put.return_value = Mock(status_code=200, text='{"k1": "v1"}')
            response = self.resource.put()
            mocked_put.assert_called_with(url=EXPECTED_URL, json=EXPECTED_DATA, params=EXPECTED_PARAMS, headers=EXPECTED_HEADERS)

    def test_patch(self):
        with patch('requests.patch') as mocked_patch:
            mocked_patch.return_value = Mock(status_code=200, text='{"k1": "v1"}')
            response = self.resource.patch()
            mocked_patch.assert_called_with(url=EXPECTED_URL, json=EXPECTED_DATA, params=EXPECTED_PARAMS, headers=EXPECTED_HEADERS)


    def test_post_json(self):
        with patch('requests.post') as mocked_post:
            mocked_post.return_value = Mock(status_code=200, text='{"k1": "v1"}')
            response = self.resource.post()
            mocked_post.assert_called_with(url=EXPECTED_URL, json=EXPECTED_DATA, params=EXPECTED_PARAMS, headers=EXPECTED_HEADERS)

    def test_post_form(self):
        with patch('requests.post') as mocked_post:
            mocked_post.return_value = Mock(status_code=200, text='{"k1": "v1"}')
            response = self.resource.post(form=True)
            mocked_post.assert_called_with(url=EXPECTED_URL, data=EXPECTED_DATA, params=EXPECTED_PARAMS, headers=EXPECTED_HEADERS)
        