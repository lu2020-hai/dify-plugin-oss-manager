## oss-manager

**Author:** haichang  
**Version:** 0.0.1  
**Type:** extension  
**Repo:** :[https://github.com/lu2020-hai/dify-plugin-oss-manager](https://github.com/lu2020-hai/dify-plugin-oss-manager)

## 简介

**OSS Manager** 是一个用于管理多种对象存储服务的工具，旨在简化开发者与不同云存储服务之间的交互。无论您使用的是 Amazon S3、阿里云 OSS 还是其他主流的对象存储服务，本工具都可以帮助您轻松完成存储桶的创建、文件的上传/下载、以及存储资源的查询和删除等操作。

---

## 功能特性

- **多平台支持**：支持多种主流对象存储服务（如 Amazon S3、阿里云 OSS、Azure Blob Storage 等）。
- **统一接口**：提供一致的 API 接口，屏蔽底层存储服务的差异。
- **灵活配置**：通过 JSON 配置文件快速连接到不同的存储服务。
- **工具集**：
  - 保存存储配置
  - 删除存储配置
  - 查询存储中的文件
  - 下载存储中的文件

---

## 支持的对象存储服务

以下是我们当前支持的对象存储服务类型：

| 类型                 | 英文名称                          | 中文名称              |
|----------------------|-----------------------------------|-----------------------|
| Amazon S3            | Amazon S3                        | 亚马逊 S3             |

## 暂不支持的对象存储服务

| 类型                 | 英文名称                          | 中文名称              |
|----------------------|-----------------------------------|-----------------------|
| Alibaba Cloud OSS    | Alibaba Cloud OSS                | 阿里云 OSS            |
| Azure Blob Storage   | Azure Blob Storage               | Azure Blob 存储       |
| Baidu Object Storage | Baidu Object Storage (BOS)       | 百度对象存储 (BOS)    |
| Google Cloud Storage | Google Cloud Storage             | 谷歌云存储            |
| Huawei Cloud OBS     | Huawei Cloud OBS                 | 华为云 OBS            |
| Oracle Cloud Storage | Oracle Cloud Infrastructure Storage | 甲骨文云基础设施存储 |
| Tencent Cloud COS    | Tencent Cloud COS                | 腾讯云 COS            |
| Volcengine TOS       | Volcengine TOS                   | 火山引擎 TOS          |

---

## 快速开始

### 配置存储服务

1. **选择存储类型**  
   在配置文件中，指定您要连接的对象存储服务类型。例如，选择 `s3` 表示使用 Amazon S3。

2. **填写配置 JSON**  
   根据所选存储类型，填写对应的配置信息。以下是一个 Amazon S3 的配置示例：

   ```json
   {
     "S3_USE_AWS_MANAGED_IAM": false,
     "S3_ENDPOINT": "https://s3.amazonaws.com",
     "S3_BUCKET_NAME": "your-bucket-name",
     "S3_ACCESS_KEY": "your-access-key",
     "S3_SECRET_KEY": "your-secret-key",
     "S3_REGION": "us-east-1"
   }
   ```