import posixpath
from collections.abc import Generator
from typing import Dict, List

import oss2 as aliyun_s3  # type: ignore

from storage.base_storage import BaseStorage
from tools.get_file_meta import infer_file_info


class AliyunOssStorage(BaseStorage):
    """Implementation for Aliyun OSS storage."""

    def __init__(self,dify_config):
        super().__init__()
        self.bucket_name = dify_config.ALIYUN_OSS_BUCKET_NAME
        self.folder = dify_config.ALIYUN_OSS_PATH
        oss_auth_method = aliyun_s3.Auth
        region = None
        if dify_config.ALIYUN_OSS_AUTH_VERSION == "v4":
            oss_auth_method = aliyun_s3.AuthV4
            region = dify_config.ALIYUN_OSS_REGION
        oss_auth = oss_auth_method(dify_config.ALIYUN_OSS_ACCESS_KEY, dify_config.ALIYUN_OSS_SECRET_KEY)
        self.client = aliyun_s3.Bucket(
            oss_auth,
            dify_config.ALIYUN_OSS_ENDPOINT,
            self.bucket_name,
            connect_timeout=30,
            region=region,
        )

    def save(self, filename, data):
        self.client.put_object(self.__wrapper_folder_filename(filename), data)

    def load_once(self, filename: str) -> bytes:
        obj = self.client.get_object(self.__wrapper_folder_filename(filename))
        data: bytes = obj.read()
        return data

    def load_stream(self, filename: str) -> Generator:
        obj = self.client.get_object(self.__wrapper_folder_filename(filename))
        while chunk := obj.read(4096):
            yield chunk

    def download(self, filename: str, target_filepath):
        self.client.get_object_to_file(self.__wrapper_folder_filename(filename), target_filepath)

    def exists(self, filename: str):
        return self.client.object_exists(self.__wrapper_folder_filename(filename))

    def delete(self, filename: str):
        self.client.delete_object(self.__wrapper_folder_filename(filename))

    def __wrapper_folder_filename(self, filename: str) -> str:
        return posixpath.join(self.folder, filename) if self.folder else filename

    def query_files(self, prefix: str = None, suffix: str = None) -> Dict[str, List[Dict[str, str]]]:
        """
        查询当前目录下的文件和子目录，并支持通过后缀过滤文件。

        :param prefix: 当前目录的路径前缀，默认为根目录。
        :param suffix: 文件后缀过滤条件，例如 ".wav"。如果为 None，则不过滤。
        :return: 包含文件和子目录的字典。
        """
        files = []
        directories = []

        query_prefix = self.__wrapper_folder_filename(prefix or "")
        delimiter = "/"

        # 使用 list_objects_v2 获取文件和目录信息
        result = self.client.list_objects(prefix=query_prefix, delimiter=delimiter)

        # 处理文件
        for obj in result.object_list:
            key = obj.key
            if not key.endswith("/"):  # 排除目录
                if suffix is None or key.endswith(suffix):
                    files.append({"name": posixpath.basename(key), "path": key})

        # 处理目录
        for common_prefix in result.prefix_list:
            prefix_key = common_prefix
            name = posixpath.basename(posixpath.normpath(prefix_key))
            directories.append({"name": name, "path": prefix_key})

        return {"file": files, "directory": directories}


    def get_file_metadata(self, filename: str) -> dict:
        """
        获取文件的元数据信息。

        :param filename: 文件名或路径。
        :return: 包含文件元数据的字典。
        """
        wrapped_filename = self.__wrapper_folder_filename(filename)

        if not self.exists(wrapped_filename):
            raise FileNotFoundError(f"File not found: {filename}")

        try:
            # 使用 head_object 获取文件元数据
            response = self.client.head_object(wrapped_filename)

            # 提取文件名和扩展名
            base_filename = posixpath.basename(filename)
            extension = posixpath.splitext(base_filename)[1]

            mime_type, file_type = infer_file_info(filename)

            # 构造元数据字典
            meta = {
                "dify_model_identity": "__dify__file__",
                "mime_type": mime_type,
                "file_type": file_type.value,
                "filename": base_filename,
                "extension": extension,
                "size": response.content_length,
            }
        except Exception as ex:
            if "NoSuchKey" in str(ex):
                raise FileNotFoundError(f"File not found: {filename}")
            else:
                raise
        return meta
