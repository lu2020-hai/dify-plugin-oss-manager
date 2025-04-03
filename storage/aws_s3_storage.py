import logging
import os
from collections.abc import Generator
from typing import Dict, List

import boto3  # type: ignore
from botocore.client import Config  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from storage.base_storage import BaseStorage
from tools.get_file_meta import infer_file_info

logger = logging.getLogger(__name__)


class AwsS3Storage(BaseStorage):
    """Implementation for Amazon Web Services S3 storage."""

    def __init__(self,dify_config):
        super().__init__()
        self.bucket_name = dify_config.S3_BUCKET_NAME
        if dify_config.S3_USE_AWS_MANAGED_IAM:
            logger.info("Using AWS managed IAM role for S3")

            session = boto3.Session()
            region_name = dify_config.S3_REGION
            self.client = session.client(service_name="s3", region_name=region_name)
        else:
            logger.info("Using ak and sk for S3")

            self.client = boto3.client(
                "s3",
                aws_secret_access_key=dify_config.S3_SECRET_KEY,
                aws_access_key_id=dify_config.S3_ACCESS_KEY,
                endpoint_url=dify_config.S3_ENDPOINT,
                region_name=dify_config.S3_REGION,
                config=Config(s3={"addressing_style": dify_config.S3_ADDRESS_STYLE}),
            )
        # create bucket
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            # if bucket not exists, create it
            if e.response["Error"]["Code"] == "404":
                self.client.create_bucket(Bucket=self.bucket_name)
            # if bucket is not accessible, pass, maybe the bucket is existing but not accessible
            elif e.response["Error"]["Code"] == "403":
                pass
            else:
                # other error, raise exception
                raise

    def save(self, filename, data):
        self.client.put_object(Bucket=self.bucket_name, Key=filename, Body=data)

    def load_once(self, filename: str) -> bytes:
        try:
            data: bytes = self.client.get_object(Bucket=self.bucket_name, Key=filename)["Body"].read()
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError("File not found")
            else:
                raise
        return data

    def load_stream(self, filename: str) -> Generator:
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=filename)
            yield from response["Body"].iter_chunks()
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError("file not found")
            elif "reached max retries" in str(ex):
                raise ValueError("please do not request the same file too frequently")
            else:
                raise

    def download(self, filename, target_filepath):
        self.client.download_file(self.bucket_name, filename, target_filepath)

    def exists(self, filename):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=filename)
            return True
        except:
            return False

    def delete(self, filename):
        self.client.delete_object(Bucket=self.bucket_name, Key=filename)

    def query_files(self, prefix: str = None, suffix: str = None) -> Dict[str, List[Dict[str, str]]]:
        """
        查询当前目录下的文件和子目录，并支持通过后缀过滤文件。

        :param prefix: 当前目录的路径前缀，默认为根目录。
        :param suffix: 文件后缀过滤条件，例如 ".wav"。如果为 None，则不过滤。
        :return: 包含文件和子目录的字典。
        """
        files = []
        directories = []

        if prefix is None:
            query_prefix = "/"
        else:
            query_prefix = prefix.rstrip("/") + "/"

        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=query_prefix,
                Delimiter="/"
            )

            for obj in response.get("Contents", []):
                key = obj["Key"]
                if not key.endswith("/"):
                    if suffix is None or key.endswith(suffix):
                        files.append({"name": key.split("/")[-1], "path": key})

            for common_prefix in response.get("CommonPrefixes", []):
                prefix_key = common_prefix["Prefix"]
                name = prefix_key.rstrip("/").split("/")[-1]
                directories.append({"name": name, "path": prefix_key})

        except ClientError as ex:
            logger.error(f"Error querying files: {ex}")
            raise

        return {"file": files, "directory": directories}

    def get_file_metadata(self, filename: str) -> dict:
        """
        获取文件的元数据信息。

        :param filename: 文件名或路径。
        :return: 包含文件元数据的字典。
        """
        if not self.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        try:
            # 使用 head_object 获取文件元数据
            response = self.client.head_object(Bucket=self.bucket_name, Key=filename)

            # 提取文件名和扩展名
            base_filename = os.path.basename(filename)
            extension = os.path.splitext(base_filename)[1]

            mime_type, file_type = infer_file_info(filename)
            # 构造元数据字典
            meta = {
                "dify_model_identity": "__dify__file__",
                "mime_type": mime_type,
                "file_type": file_type.value,
                "filename": base_filename,
                "extension": extension,
                "size": response.get("ContentLength", 0),
            }
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File not found: {filename}")
            else:
                raise
        return meta

