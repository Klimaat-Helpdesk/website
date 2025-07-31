from storages.backends.s3 import S3Storage


class StaticS3Storage(S3Storage):
    querystring_auth = False
    """
    Querystring auth must be disabled so that url() returns a consistent output.
    This makes browser cache possible and links always available (useful for emails)
    """

    file_overwrite = True
    """File overwrite must be enabled so that assets like images are not duplicated"""

    location = "static"
    """Prefix path"""

    default_acl = "public-read"
    """
    Set file ACL to public. This is ignored by Minio and most other providers,
    because they only use policies. Some providers (Exoscale) only support ACL.
    """

    def exists(self, name):
        """The collectstatic --clear option, does a check on an empty string.

        S3 does not support this, so we return True.
        """
        if name == "":
            return True

        return super().exists(name)


class MediaS3Storage(S3Storage):
    querystring_auth = False
    """
    Querystring auth must be disabled so that url() returns a consistent output.
    This makes browser cache possible and links always available (useful for emails)
    """

    file_overwrite = False
    """File overwrite must be disabled so that users can upload files with same name"""

    location = "media"
    """Prefix path"""

    default_acl = "public-read"
    """
    Set file ACL to public. This is ignored by Minio and most other providers,
    because they only use policies. Some providers (Exoscale) only support ACL.
    """
