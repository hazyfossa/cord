from enum import StrEnum
from typing import Any

from pyoci.common import Struct


class OciDistributionErrorCode(StrEnum):
    BLOB_UNKNOWN = "BLOB_UNKNOWN"
    BLOB_UPLOAD_INVALID = "BLOB_UPLOAD_INVALID"
    BLOB_UPLOAD_UNKNOWN = "BLOB_UPLOAD_UNKNOWN"
    DIGEST_INVALID = "DIGEST_INVALID"

    MANIFEST_BLOB_UNKNOWN = "MANIFEST_BLOB_UNKNOWN"
    MANIFEST_INVALID = "MANIFEST_INVALID"
    MANIFEST_UNKNOWN = "MANIFEST_UNKNOWN"

    NAME_INVALID = "NAME_INVALID"
    NAME_UNKNOWN = "NAME_UNKNOWN"

    SIZE_INVALID = "SIZE_INVALID"

    UNAUTHORIZED = "UNAUTHORIZED"
    DENIED = "DENIED"
    UNSUPPORTED = "UNSUPPORTED"
    TOOMANYREQUESTS = "TOOMANYREQUESTS"


class Error(Struct):
    code: OciDistributionErrorCode
    message: str
    details: Any  # unstructured
