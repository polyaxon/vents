from typing import Optional

from s3fs import S3FileSystem as BaseS3FileSystem

from vents.providers.aws.service import AWSService


S3_CONNECT_TIMEOUT = 30
S3_READ_TIMEOUT = 120
S3_MAX_POOL_CONNECTIONS = 50


class S3FileSystem(BaseS3FileSystem):
    retries = 3
    connect_timeout = S3_CONNECT_TIMEOUT
    read_timeout = S3_READ_TIMEOUT


class S3Service(AWSService):
    def _set_session(
        self,
        asynchronous: Optional[bool] = False,
        use_listings_cache: Optional[bool] = False,
        **kwargs,
    ):
        config_kwargs = dict(kwargs.pop("config_kwargs", {}) or {})
        if self.region and "region_name" not in config_kwargs:
            config_kwargs["region_name"] = self.region
        config_kwargs.setdefault("request_checksum_calculation", "when_required")
        config_kwargs.setdefault("response_checksum_validation", "when_required")
        config_kwargs.setdefault("connect_timeout", S3_CONNECT_TIMEOUT)
        config_kwargs.setdefault("read_timeout", S3_READ_TIMEOUT)
        config_kwargs.setdefault("max_pool_connections", S3_MAX_POOL_CONNECTIONS)
        client_kwargs = dict(kwargs.pop("client_kwargs", {}) or {})
        if self.verify_ssl is not None and "verify" not in client_kwargs:
            client_kwargs["verify"] = self.verify_ssl
        self._session = S3FileSystem(
            key=self.access_key_id,
            secret=self.secret_access_key,
            token=self.session_token,
            use_ssl=self.use_ssl,
            endpoint_url=self.endpoint_url,
            config_kwargs=config_kwargs,
            client_kwargs=client_kwargs,
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs,
        )

    def get_fs(
        self,
        asynchronous: Optional[bool] = False,
        use_listings_cache: Optional[bool] = False,
        **kwargs,
    ):
        self._set_session(
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs,
        )
        return self.session
