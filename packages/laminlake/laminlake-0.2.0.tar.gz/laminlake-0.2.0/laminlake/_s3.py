import boto3
from pathlib import Path
import anndata

# remote bucket
s3 = boto3.resource("s3")
bucket_name = "lamin0"
bucket = s3.Bucket(bucket_name)

# local cache directory
cache = Path.home() / "cache"
if not cache.exists():
    cache.mkdir()


class File:
    """Access shared file storage.

    Params
    ------
    sid
        String representing semantic identifier.
    """

    def __init__(self, sid: str):
        self._sid = sid
        self._cache = cache / self._sid

    def pull(self):
        """Pull file."""
        bucket.download_file(self._sid, self._cache.as_posix())

    def load(self):
        """Load file."""
        if not self._cache.exists():
            self.pull()
        return anndata.read(self._cache)

    def push(self, path):
        """Push file."""
        return bucket.upload_file(path, self._sid)
