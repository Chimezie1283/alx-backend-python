#!/usr/bin/env python3
"""Test for the clinet module"""
import unittest
from unittest.mock import PropertyMock, patch
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """test GithubOrgClient class"""

    @parameterized.expand(
        [
            ("google", {"org": "google"}),
            ("abc", {"org": "abc"}),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, output, mock_get_json):
        """test that GithubOrgClient.org returns the correct value"""
        test_init = GithubOrgClient(org_name)
        mock_get_json.return_value = output
        self.assertEqual(output, test_init.org)
        mock_get_json.assert_called_once()

    @patch("client.get_json")
    def test_public_repos_url(self, mock_get_json):
        """test client.get_json to check the _public_repos_url behavior"""
        test_init = GithubOrgClient("test")
        output = {"repos_url": "www.test.com"}
        mock_get_json.return_value = output
        self.assertEqual(test_init._public_repos_url, output["repos_url"])

    @patch("client.get_json")
    @patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock,
    )
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """test public_repos using PropertyMock"""
        test_instance = GithubOrgClient("test")
        mock_public_repos_url.return_value = "www.test.com"
        repos_list = {"repos": ["r1", "r2", "r3", "...etc"]}
        mock_get_json.return_value = repos_list
        self.assertEqual(test_instance.repos_payload, repos_list)
        mock_get_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, output):
        """test has_license"""
        has_license = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(has_license, output)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient
    """

    class setUpClass:
        """
        Set up class for integration test
        """

        @patch("client.get_json")
        def setUp(self, mock_get_json):
            """
            Set up method for class
            """
            self.test_class = GithubOrgClient("test")
            self.org_payload = {"repos_url": "www.test.com"}
            self.repos_payload = [
                {"name": "repo1", "license": {"key": "my_license"}},
                {"name": "repo2", "license": {"key": "other_license"}},
            ]
            mock_get_json.side_effect = [
                self.org_payload,
                self.repos_payload,
            ]


@parameterized_class(

    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Class for Integration test of fixtures"""

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        config = {
            "return_value.json.side_effect": [
                cls.org_payload,
                cls.repos_payload,
                cls.org_payload,
                cls.repos_payload,
            ]
        }
        cls.get_patcher = patch("requests.get", **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """Integration test for public repos with License"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos("apache-2.0"),
                         self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
