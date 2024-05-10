#!/usr/bin/env python3
"""Test for the utils module"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import MagicMock, patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class"""

    @parameterized.expand(
        [
            ({"a": 1}, "a", 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, output) -> None:
        """test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), output)

    @parameterized.expand(
        [
            ({}, ("a",), KeyError),
            ({"a": 1}, ("a", "b"), KeyError),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, error):
        """test access_nested_map using invalid inputs"""
        with self.assertRaises(error):
            self.assertEqual(access_nested_map(nested_map, path))


class TestGetJson(unittest.TestCase):
    """Class for Testing Get Json"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_requests_get) -> None:
        """test get_json using by patching requests.getreturn test_payload"""
        mock_json = Mock(return_value=test_payload)
        mock_requests_get.return_value.json = mock_json
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_requests_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Class for Testing Memoize"""

    def test_memoize(self):
        """Test memoize"""

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method") as mock_a_method:
            mock_a_method.return_value = 10

            instance_of_test_class = TestClass()
            res = instance_of_test_class.a_property
            self.assertEqual(instance_of_test_class.a_property, res)
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
