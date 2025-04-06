from enum import Enum

# 定义 FileType 枚举类
class FileType(Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    ARCHIVE = "archive"  # 新增：用于压缩文件
    CODE = "code"        # 新增：用于代码文件
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
    ".md": "text/markdown",  # 新增：Markdown 文件
    ".zip": "application/zip",
    ".rar": "application/x-rar-compressed",
    ".csv": "text/csv",
    ".json": "application/json",
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".svg": "image/svg+xml",
}

# 定义 MIME 类型到 FileType 的映射（新增映射）
MIME_TO_FILE_TYPE = {
    "image/jpeg": FileType.IMAGE,
    "image/png": FileType.IMAGE,
    "image/gif": FileType.IMAGE,
    "image/bmp": FileType.IMAGE,
    "image/svg+xml": FileType.IMAGE,  # SVG 图像
    "application/pdf": FileType.DOCUMENT,
    "application/msword": FileType.DOCUMENT,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": FileType.DOCUMENT,
    "application/vnd.ms-excel": FileType.DOCUMENT,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": FileType.DOCUMENT,
    "application/vnd.ms-powerpoint": FileType.DOCUMENT,
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": FileType.DOCUMENT,
    "text/plain": FileType.DOCUMENT,
    "text/markdown": FileType.DOCUMENT,  # Markdown 文件
    "text/csv": FileType.DOCUMENT,       # CSV 文件
    "application/json": FileType.DOCUMENT,  # JSON 文件
    "text/html": FileType.DOCUMENT,      # HTML 文件
    "text/css": FileType.CODE,           # CSS 文件
    "application/javascript": FileType.CODE,  # JavaScript 文件
    "audio/mpeg": FileType.AUDIO,
    "audio/wav": FileType.AUDIO,
    "video/mp4": FileType.VIDEO,
    "video/x-msvideo": FileType.VIDEO,
    "video/x-matroska": FileType.VIDEO,
    "application/zip": FileType.ARCHIVE,  # ZIP 压缩文件
    "application/x-rar-compressed": FileType.ARCHIVE,  # RAR 压缩文件
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