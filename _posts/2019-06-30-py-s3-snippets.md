---
title: "Useful S3 Python Snippets"
date: 2019-06-30T00:00:00-00:00
last_modified_at: 2019-06-30T00:00:00-00:00
categories:
  - software notes
permalink: /post-py-s3-snippets/
classes: wide
toc: true
excerpt: A collection of useful actions when interacting w/ s3 in python.
header:
  og_image: https://logicoretech.com/wp-content/uploads/2022/05/Python-Symbol.png
  teaser: https://logicoretech.com/wp-content/uploads/2022/05/Python-Symbol.png
---


## Key manipulation

I like to deal with keys in the format `s3://<bucket-name>/path/to/file.ext`.

Some validation helpers are always useful:

```py
S3_PREFIX = "s3://"

def is_s3_path(s3_path: str, s3_prefix: str = S3_PREFIX)->bool:
    return s3_path.startswith(s3_prefix)
```

This makes it easy to handle arbitrary input uris be they local file paths or remote s3 paths.

Many actions require parsing a bucket-name and or a key suffix:

```py

def sanitize_separators(s: str) -> str:
    return s.replace("\\", "/")

def split_s3_path(s3_path: str)->Tuple[str, str]:
    """
    Parameters:
        s3_path (str): an s3 path in the format of s3://<bucket-name>/path/to/key
    Returns:
        Tuple[str,str]: (bucket name, key)
        example:
            split_s3_path("s3://some-bucket/path/to/image.jpg") -> ("some-bucket", "path/to/image.jpg")
    """
    assert is_s3_path(
        s3_path
    ), f"Expected s3 path in the form {S3_PREFIX}<bucket>/path/to/key"

    s3_path = s3_path.lstrip(S3_PREFIX)
    all_parts = []
    while 1:
        parts = osp.split(s3_path)
        if parts[0] == s3_path:  # sentinel for absolute paths
            all_parts.insert(0, parts[0])
            break
        elif parts[1] == s3_path:  # sentinel for relative paths
            all_parts.insert(0, parts[1])
            break
        else:
            s3_path = parts[0]
            all_parts.insert(0, parts[1])
    
    return all_parts[0], sanitize_separators(
        osp.join(*all_parts[1:]) if len(all_parts) > 1 else ""
    )
```

## Client Control

I like to control credentials and other defaults through environment variables.

```py
# Ex: "http://localhost:30000"
S3_ENDPOINT = os.getenv("S3_ENDPOINT", None)

def get_default_s3_client(endpoint_url:str=None)->boto3.client:
    if endpoint_url is None:
        endpoint_url = S3_ENDPOINT if S3_ENDPOINT else None
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
    )
```

## Basic IO

Checking if a file exists:

```py
def key_exists(s3_path: str, client=None) -> bool:
    assert is_s3_path(
        s3_path
    ), f"Expected s3 path in the form {S3_PREFIX}<bucket>/path/to/key"
    if client is None:
        client = get_default_s3_client()
    s3_bucket, s3_key = split_s3_path(s3_path)

    response = client.list_objects_v2(
        Bucket=s3_bucket,
        Prefix=s3_key,
    )
    for obj in response.get("Contents", []):
        if obj["Key"] == s3_key:
            return True

    return False
```

Check if a directory exists:

```py
def dir_exists(s3_path: str, client=None) -> bool:
    # Folder should exist, but can be empty
    assert is_s3_path(
        s3_path
    ), f"Expected s3 path in the form {S3_PREFIX}<bucket>/path/to/key"
    if client is None:
        client = get_default_s3_client()
    s3_bucket, s3_key = split_s3_path(s3_path)
    s3_key = s3_key.rstrip("/")
    resp = client.list_objects(
        Bucket=s3_bucket, Prefix=s3_key, Delimiter="/", MaxKeys=1
    )
    return "CommonPrefixes" in resp
```

Read the bytes of a file:

```py
def read_file_s3(s3_path: str, client=None, encoding: str = None) -> str:
    assert is_s3_path(
        s3_path
    ), f"Expected s3 path in the form {S3_PREFIX}<bucket>/path/to/key"
    if client is None:
        client = get_default_s3_client()
    s3_bucket, s3_key = split_s3_path(s3_path)
    response = client.get_object(Bucket=s3_bucket, Key=s3_key)
    body = response["Body"].read()
    if encoding:
        return body.decode(encoding)
    return body
```

For example, you can load a JSON file from s3 in memory:

```py
def load_json_s3(s3_path: str, client=None)->Dict:
    return json.loads(
        read_file_s3(s3_path=s3_path, client=client).decode("utf-8")
    )
```

Or open an image from s3 in memory:

```py
# PIL Variant
def imread(s3_path: str, client=None):
    buf = read_file_s3(s3_path=s3_path, client=client)
    return Image.open(BytesIO(buf))

# OpenCV Variant
def imread(s3_path: str, client=None, read_style=cv2.IMREAD_UNCHANGED):
    buf = read_file_s3(s3_path=s3_path, client=client)
    im = cv2.imdecode(np.frombuffer(buf), read_style)
    assert im is not None, s3_path
    return im
```

Downloading a file to disk:

```py
def download_file(s3_path: str, dst_path: str, client=None):
    assert is_s3_path(
        s3_path
    ), f"Expected path in the form {S3_PREFIX}<bucket>/path/to/key.ext"

    if client is None:
        client = get_default_s3_client()
    bucket, key = split_s3_path(s3_path)

    with open(dst_path, "wb") as f:
        client.download_fileobj(bucket, key, f)
```


Uploading a local file to s3:

```py
def upload_file_to_s3(src_path: str, s3_path: str, client=None):
    assert osp.isfile(src_path), f"{src_path} does NOT exist."
    assert is_s3_path(
        s3_path
    ), f"Expected path in the form {S3_PREFIX}<bucket>/path/to/file"
    if client is None:
        client = get_default_s3_client()
    bucket, key = split_s3_path(s3_path)
    client.upload_file(src_path, bucket, key)

def upload_file_object_to_s3(file_obj, s3_path: str, client=None):
    assert is_s3_path(
        s3_path
    ), f"Expected path in the form {S3_PREFIX}<bucket>/path/to/"
    if client is None:
        client = get_default_s3_client()
    bucket, key = split_s3_path(s3_path)
    logger.info(f"Uploading file obj to {s3_path}")
    client.upload_fileobj(file_obj, bucket, key)
```

Uploading a local directory to s3:

```py
def upload_local_directory_to_s3(
    input_dir: str, s3_path: str, client=None, exist_ok: bool = False
):
    assert is_s3_path(
        s3_path
    ), f"Expected path in the form {S3_PREFIX}<bucket>/path/to/"

    if client is None:
        client = get_default_s3_client()

    s3_path = sanitize_separators(s3_path)
    s3_path = s3_path if s3_path.endswith("/") else s3_path + "/"
    if not exist_ok:
        assert not key_exists(
            s3_path=s3_path, client=client
        ), "Destination path already exists!"

    for local_path, sub_dirs, files in os.walk(input_dir):
        for fname in files:
            src_path = osp.join(local_path, fname)
            rel_path = osp.relpath(src_path, input_dir)
            dst_s3_path = sanitize_separators(osp.join(s3_path, rel_path))
            upload_file_to_s3(src_path=src_path, s3_path=dst_s3_path, client=client)
```

## Searching files in s3

```py
def get_matching_s3_objects(
    bucket: str, prefix: str = "", suffix: str = "", client=None
) -> Generator:
    """
    Generate objects in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with this prefix (optional).
    :param suffix: Only fetch objects whose keys end with this suffix (optional).
    """
    if client is None:
        client = get_default_s3_client()
    paginator = client.get_paginator("list_objects_v2")

    kwargs = {"Bucket": bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix,)
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = sanitize_separators(key_prefix)

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                break

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket: str, prefix: str = "", suffix: str = "", client=None) -> Generator[str]:
    """
    Generate the keys in an S3 bucket.
    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    if client is None:
        client = get_default_s3_client()
    for obj in get_matching_s3_objects(
        client=client, bucket=bucket, prefix=prefix, suffix=suffix
    ):
        yield obj["Key"]


def get_immediate_subdirs(
    s3_path: str,
    client=None,
) -> List[str]:
    """Gets the immediate subdirectory names
    Args:
        s3_path [str]:
        client: the s3 cient
    Returns:
        [List[str]]: a collection of names for any immediate subdirectories
    """
    assert is_s3_path(
        s3_path
    ), f"Expected path in the form {S3_PREFIX}<bucket>/path/to/dir/"

    if client is None:
        client = get_default_s3_client()

    bucket, prefix = split_s3_path(s3_path)
    if prefix and not prefix.endswith("/"):
        prefix += "/"

    paginator = client.get_paginator("list_objects_v2")
    subdirs = set()
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        prefixes = page.get("CommonPrefixes", [])
        for prefix in prefixes:
            prefix_name = prefix["Prefix"]
            if prefix_name.endswith("/"):
                subdir = prefix_name.rstrip("/")
                subdirs.add(subdir.split("/")[-1])

    return list(subdirs)
```

## Adding simple caching

A very simple caching decorator based on a least-recently used cache. 
```py
from functools import lru_cache

DEFAULT_CACHE_DIRECTORY = os.getenv("MY_S3_DATA_CACHE_DIRECTORY", None)
CACHE_MEMORY = (
    Memory(
        location=DEFAULT_CACHE_DIRECTORY,
        verbose=0,
        mmap_mode=None,
    )
    if DEFAULT_CACHE_DIRECTORY
    else None
)

def _optional_cache_decorator():
    def decorator(func):
        if DEFAULT_CACHE_DIRECTORY:
            # Return caching
            return CACHE_MEMORY.cache(func)
        # No caching... return the function unchanged
        return func

    return decorator
```

The above decorator can be useful when repeatedly pulling the same data from s3 - for example, a dataloader used during a model training routine. Take the example of an image data loader. Applying the caching decorator to the "read file" operation will cache the raw file data stored in s3... which likely represents compressed "jpeg" binary data. Downstream utilities like "imread" which yield dramaticcally larger structures (image arrays or tensors) can repeat the minimal last-mile work decoding the image from the cache. For example:

```py
@_optional_cache_decorator()
def read_file_s3(s3_path: str, client=None, encoding: str = None) -> str:
    ...

def imread(s3_path: str, client=None):
    buf = read_file_s3(s3_path=s3_path, client=client)
    return Image.open(BytesIO(buf))
```

## AsyncIO

Depending on the situation, it can be much faster to leverage async variants:

```py
# Basic IO
async def download_object(s3_path: str, client, sem):
    """Downloads an object from s3"""
    assert is_s3_path(
        s3_path
    ), f"Expected path in the form {S3_PREFIX}<bucket>/path/to/key.ext"
    bucket, key = split_s3_path(s3_path)
    async with sem:
        # get object from s3
        response = await client.get_object(Bucket=bucket, Key=key)

        # this will ensure the connection is correctly re-used/closed
        async with response["Body"] as stream:
            return await stream.read()

async def save_object(s3_path: str, output_path: str, client, sem):
    """Download an object from s3 and saves it to disk"""
    data = await download_object(s3_path=s3_path, client=client, sem=sem)
    os.makedirs(osp.dirname(output_path), exist_ok=True)
    async with aiofiles.open(output_path, "wb") as f:
        await f.write(data)
```

For example, downloading many files concurrently significantly outperforms the AWS CLI:

```py
s3_uris = ...
client = aiobotocore.AioSession().create_client("s3")
sem = asyncio.Semaphore(min(len(s3_uris), 25))
await asyncio.gather(
    *[
        save_object(
            s3_path=uri,
            output_path=osp.join("output", osp.basename(uri)),
            client=s3_client,
            sem=sem,
        )
        for uri in uris
    ]
)
```
