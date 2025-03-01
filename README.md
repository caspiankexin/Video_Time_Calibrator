# Video_Time_Calibrator

📅 时间：2025年2月28日   
👨‍💻 作者GitHub：@caspiankexin   
📨 作者邮箱： [联系我](mailto:mirror_flower@outlook.com)  
📢 项目地址：[Video_Time_Calibrato](https://github.com/caspiankexin/Video_Time_Calibrator)
⏬ 下载地址：[资源导航页](https://flowus.cn/cckeker/share/85efac3f-a20d-4f36-b68a-410decf4f6da) 
✳️ 转载至：原创  

---
# 问题描述

## 相册时间墙

相册平台在展示内容时，一般都会以时间流的形式来展现，以时间顺序来罗列照片。我认为这是相册软件最大的作用。

相册软件对于照片日期的认定是通过照片、视频的exif信息来判断的。图片一般是“拍摄日期”，视频一般是“媒体创建日期”。

但是因为各种软件，会存在一些视频的“媒体创建日期”丢失或错误，导致相册平台的视频时间错乱，所以需要人工修改核对照片的“媒体创建日期”，确保在照片平台时间线正确。

## 不同相册平台时间展示逻辑

图片一般都是按照“拍摄日期”来认定时间。

视频有不同策略，主要分为“媒体创建日期”和“修改日期”两种。表格是我测试得出的，不全面。

| 平台       | 时间认定方式 |
| -------- | ------ |
| 谷歌相册     | 媒体创建日期 |
| OneDrive | 媒体创建日期 |
| 天翼相册     | 媒体创建日期 |
| 华为云相册    | 修改日期   |
|          |        |
|          |        |
## 需求及使用场景

需求就是保证视频在不同相册平台的时间信息都是准确一致的，这就要求视频exif元数据中所有时间信息保持一致。对于“媒体创建日期”丢失及错误的文件，要清晰筛选出来，以便我手动对照修改。

关于“媒体创建日期”需要快速修改的情况，此次不涉及，可以下面exiftool工具介绍部分了解，自己研究。（因为我认为视频的准备日期需要用户翻看回忆一一确定，不存在批量修改的场景。）

# 视频文件exif时间信息

## Windows文件管理器读取的信息

*在文件“属性”→“详细信息”查看*

- 创建日期 
- 修改日期（部分相册平台的时间依据）
- 创建媒体日期（相册平台的时间依据）

## exiftool读取的信息

*通过 `exiftool 文件名.mp4` 命令查看*

- File Creation Date/Time 
- File Modification Date/Time
- Create Date
- Modify Date
- Track Create Date
- Track Modify Date
- Media Create Date
- Media Modify Date

## 文件管理器和exiftool的相互对应及含义

| 文件管理器  | exiftool信息                  |
| ------ | --------------------------- |
| 媒体创建日期 | Create Date                 |
| 创建日期   | File Creation Date/Time     |
| 修改日期   | File Modification Date/Time |

其余的`Modify Date`、`Track Create Date`、`Track Modify Date`、`Media Create Date`、`Media Modify Date`等信息，经过实验比对，记录的都是视频的拍摄日期，也就是“`媒体创建日期`”/“`Create Date`”。

# 通过exiftool处理视频exif信息

## exiftool基本介绍

ExifTool 是一款功能强大的跨平台开源工具，主要用于读取、编辑和管理多种文件格式中的元数据（metadata）。官网下载地址：[ExifTool by Phil Harvey](https://exiftool.org/) ，下载的文件解压缩后，将`exiftool(-k).exe`修改为`exiftool.exe`。

## exiftool使用方法

在`exiftool.exe`所在文件夹内点击右键的`在终端中打开`，然后输入命令来操作，如果报错的话，可以尝试修改命令为`./exiftool  具体命令`。

### 查看元数据

- `exiftool 文件名.jpg`          # 查看所有元数据
- `exiftool -TAG 文件名.jpg`     # 查看指定标签（如 `-CreateDate`、`-GPSPosition`）
- `exiftool -s 文件名.jpg`       # 以简短格式显示标签名

### 删除元数据

- `exiftool -all= 文件名.jpg`    # 删除所有元数据（保留文件结构）
- `exiftool -exif= 文件名.jpg`   # 仅删除 EXIF 数据

### 修改元数据

- `exiftool -TAG="值" 文件名.jpg`  # 修改指定标签的值
- 示例：`exiftool -DateTimeOriginal="2023:01:01 12:00:00" photo.jpg`  # 修改拍摄时间

### 批量处理

- `exiftool -命令 目录名/`        # 处理目录下所有文件
- `exiftool -r -命令 目录名/ `   # 递归处理子目录
- 示例：`exiftool -all= -r /path/to/photos/`  # 批量删除所有元数据
- `exiftool -TAG="值" *.jpg`  # 批量处理所有jpg文件

# 软件使用方法

前往文头的下载地址下载压缩文件，解压缩，确保exiftool文件和视频时间校准统一工具在一个文件夹下面。

打开工具，选择需要操作的视频所在的文件夹，然后开始处理，软件就会将视频文件的所有的时间信息全部修改为`媒体创建日期`，对于`媒体创建日期`丢失的文件，会在文件前加上`无效时间`的前缀。

注意：操作前，请做好文件备份，以免丢失。

---

如果对您有帮助，感谢打赏！🙇‍♀️🤗🫡

![](https://pub-33f36ca1f5fa4ac784111b0d3c3cd381.r2.dev/2025/02/303b772de64207e28de06464675078b4.webp)
