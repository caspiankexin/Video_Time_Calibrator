# 媒体文件时间校准统一工具（Media File Time Calibrator）

---

📅 时间：2025年2月28日   
👨‍💻 作者GitHub：@caspiankexin   
📨 作者邮箱： [联系我](mailto:mirror_flower@outlook.com)  
📢 项目地址：[Media File Time Calibrator](https://github.com/caspiankexin/Video_Time_Calibrator)  
⏬ 下载地址：[资源导航页](https://flowus.cn/cckeker/share/85efac3f-a20d-4f36-b68a-410decf4f6da)   
✳️ 转载至：原创  

---
# 软件教程

## 软件功能描述

- 软件可以处理mp4、MP4、jpg、JPG、jpeg、heic格式的文件。
- 以文件拍摄日期来修改其他时间信息，并重命名。
- 文件名后加MD5值的前六位，避免时间相同导致文件名冲突。
- 在重复的文件前加上“重复文件”字样，给予提示。
- 如需处理其他格式文件，请访问GitHub地址，查看说明。

## 使用方法

1. 前往文头的下载地址下载压缩文件，解压缩，确保exiftool文件和视频时间校准统一工具在一个文件夹下面。

2. 打开工具，选择需要操作的文件所在的文件夹，然后开始处理，软件就会将视频、照片文件的所有的时间信息全部修改为“拍摄日期”，对于“拍摄日期”丢失的文件，会在文件前加上`无效时间`的前缀。

## 拓展支持文件格式的方法

1. 在`def get_metadata(file_path, type):`部分添加需要处理的格式，并选择合适的`exif元数据`作为修改依据。
2. 在`def process_videos():`中，修改`if file_path.suffix in [".mp4", ".jpeg", ".heic", ".jpg", ".JPG", ".MP4" , ".HEIC"]:`，将需要处理的格式添加进去。
3. 在`def process_videos():`中，仿照jpg格式，添加新的代码，即可。

注意：操作前，请做好文件备份，以免丢失。
 
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
## 需求及使用场景

需求就是保证视频在不同相册平台的时间信息都是准确一致的，这就要求视频exif元数据中所有时间信息保持一致。对于“媒体创建日期”丢失及错误的文件，要清晰筛选出来，以便我手动对照修改。

关于“媒体创建日期”需要快速修改的情况，此次不涉及，可以下面exiftool工具介绍部分了解，自己研究。（因为我认为视频的准备日期需要用户翻看回忆一一确定，不存在批量修改的场景。）

# 视频、图片文件exif时间信息

## 视频文件exif信息

### Windows文件管理器读取的信息

*在文件“属性”→“详细信息”查看*

- 创建日期 
- 修改日期（部分相册平台的时间依据）
- 创建媒体日期（相册平台的时间依据）

### exiftool读取的信息

*通过 `exiftool 文件名.mp4` 命令查看*

File Creation Date/Time 、 File Modification Date/Time、Create Date、Modify Date、Track Create Date、Track Modify Date、Media Create Date、Media Modify Date

### 文件管理器和exiftool的相互对应及含义

| 文件管理器  | exiftool信息                  |
| ------ | --------------------------- |
| 媒体创建日期 | Create Date                 |
| 创建日期   | File Creation Date/Time     |
| 修改日期   | File Modification Date/Time |

对于mp4文件，优先采用`Create Date`来作为拍摄日期，但是部分视频文件`Create Date`信息为0000，无奈也可以考虑文件`File Modification Date/Time`信息也大概率就是拍摄日期，所以其次用`File Modification Date/Time`信息来作为拍摄日期，==**这就需要在处理文件前先大致坚持一下文件修改日期有没有太大问题，且文件处理后进行检查。**==

其余的`Modify Date`、`Track Create Date`、`Track Modify Date`、`Media Create Date`、`Media Modify Date`等信息，经过实验比对，记录的都是视频的拍摄日期，也就是“`媒体创建日期`”/“`Create Date`”。

## 图片文件exif信息

### Windows文件管理器读取的信息

*在文件“属性”→“详细信息”查看*

- 创建日期 
- 修改日期
- 拍摄日期（相册平台的时间依据）

### exiftool读取的信息

*通过 `exiftool 文件名.jpg` 命令查看*，主要有以下时间信息：File Creation Date/Time 、 File Modification Date/Time、Modify Date、Date/Time Original、Create Date。

### 时间信息分析

exiftool读取的时间文件中，理论上应该和视频一样，`Create Date`对应的是图片的`拍摄日期`，二者对别，也确实能对应上，但是实际操作过程中，很多图片文件（一般是第三方相机软件的照片）明明有`拍摄日期`，但是exiftool却读不出来`Create Date`。

经过试验，发现这些图片在未修改过`拍摄日期`前，只有`Date/Time Original`，修改过后，才会出现`Create Date`。查资料了解到`Date/Time Original`储存的是照片的最初拍照日期，虽然`Date/Time Original`和`Create Date`的时间信息是一致的（但是也发现部分图片二者信息不对应，有几小时差别，怀疑是时区问题）。

但是，又发现有些照片文件`Date/Time Original`不存在，这种情况就让exiftool去读取`Create Date`信息来作为拍摄日期。（只能说这些媒体文件的情况也太复杂了）

所以最后在软件上，对于jpg格式的图片，先采用`Date/Time Original`信息作为拍摄信息进行修改，再考虑`Create Date`信息作为拍摄信息进行修改。

# 通过exiftool处理文件exif信息

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

### 按照文件名修改拍摄日期

- `exiftool.exe '-FileCreateDate<filename' *.jpg` //将文件名中的时间设置为文件创建时间 
- `exiftool.exe '-FileModifyDate<filename' *.jpg` //将文件名中的时间设置为文件修改时间

---

如果对您有帮助，感谢打赏！🙇‍♀️🤗🫡

![](https://pub-33f36ca1f5fa4ac784111b0d3c3cd381.r2.dev/2025/02/303b772de64207e28de06464675078b4.webp)
