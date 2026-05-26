from unittest import TestCase
from unittest.mock import patch

from vents.providers.aws.s3 import (
    S3_CONNECT_TIMEOUT,
    S3_MAX_POOL_CONNECTIONS,
    S3_READ_TIMEOUT,
    S3Service,
)


class TestS3Service(TestCase):
    @patch("vents.providers.aws.s3.S3FileSystem")
    def test_get_fs_sets_s3_defaults(self, mock_s3_file_system):
        service = S3Service(
            access_key_id="key",
            secret_access_key="secret",
            session_token="token",
            region="us-east-1",
            endpoint_url="https://s3.example.com",
            use_ssl=True,
            verify_ssl=False,
        )

        session = service.get_fs()

        assert session == mock_s3_file_system.return_value
        mock_s3_file_system.assert_called_once_with(
            key="key",
            secret="secret",
            token="token",
            use_ssl=True,
            endpoint_url="https://s3.example.com",
            config_kwargs={
                "region_name": "us-east-1",
                "request_checksum_calculation": "when_required",
                "response_checksum_validation": "when_required",
                "connect_timeout": S3_CONNECT_TIMEOUT,
                "read_timeout": S3_READ_TIMEOUT,
                "max_pool_connections": S3_MAX_POOL_CONNECTIONS,
            },
            client_kwargs={"verify": False},
            asynchronous=False,
            use_listings_cache=False,
        )

    @patch("vents.providers.aws.s3.S3FileSystem")
    def test_get_fs_preserves_explicit_s3_config(self, mock_s3_file_system):
        service = S3Service(region="us-east-1", verify_ssl=False)

        service.get_fs(
            asynchronous=True,
            use_listings_cache=True,
            config_kwargs={
                "region_name": "eu-west-1",
                "request_checksum_calculation": "when_supported",
                "response_checksum_validation": "when_supported",
                "connect_timeout": 1,
                "read_timeout": 2,
                "max_pool_connections": 3,
            },
            client_kwargs={"verify": True},
            default_fill_cache=False,
        )

        mock_s3_file_system.assert_called_once_with(
            key=None,
            secret=None,
            token=None,
            use_ssl=None,
            endpoint_url=None,
            config_kwargs={
                "region_name": "eu-west-1",
                "request_checksum_calculation": "when_supported",
                "response_checksum_validation": "when_supported",
                "connect_timeout": 1,
                "read_timeout": 2,
                "max_pool_connections": 3,
            },
            client_kwargs={"verify": True},
            asynchronous=True,
            use_listings_cache=True,
            default_fill_cache=False,
        )
