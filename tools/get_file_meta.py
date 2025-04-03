from enum import Enum

# 定义 FileType 枚举类
class FileType(Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    CUSTOM = "custom"

# 定义扩展名到 MIME 类型的映射
EXTENSION_TO_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
    ".txt": "text/plain",
}

# 定义 MIME 类型到 FileType 的映射
MIME_TO_FILE_TYPE = {
    "image/jpeg": FileType.IMAGE,
    "image/png": FileType.IMAGE,
    "image/gif": FileType.IMAGE,
    "image/bmp": FileType.IMAGE,
    "application/pdf": FileType.DOCUMENT,
    "application/msword": FileType.DOCUMENT,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": FileType.DOCUMENT,
    "application/vnd.ms-excel": FileType.DOCUMENT,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": FileType.DOCUMENT,
    "application/vnd.ms-powerpoint": FileType.DOCUMENT,
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": FileType.DOCUMENT,
    "audio/mpeg": FileType.AUDIO,
    "audio/wav": FileType.AUDIO,
    "video/mp4": FileType.VIDEO,
    "video/x-msvideo": FileType.VIDEO,
    "video/x-matroska": FileType.VIDEO,
    "text/plain": FileType.DOCUMENT,
}

def infer_file_info(filename: str):
    """
    根据文件名推断 MIME 类型和文件类型。

    :param filename: 文件名（包含扩展名）
    :return: (mime_type, file_type) 元组
    """
    # 提取扩展名
    extension = "." + filename.split(".")[-1].lower() if "." in filename else None

    # 根据扩展名获取 MIME 类型
    mime_type = EXTENSION_TO_MIME.get(extension, "application/octet-stream")

    # 根据 MIME 类型推断文件类型
    file_type = MIME_TO_FILE_TYPE.get(mime_type, FileType.CUSTOM)

    return mime_type, file_type