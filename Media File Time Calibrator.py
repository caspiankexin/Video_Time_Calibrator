import hashlib
import subprocess
from datetime import datetime
import pytz
from pathlib import Path
import os
import tkinter as tk
from PIL import Image, ImageTk
import sys

def convertDate(MediaCreateDateText):
    # 截取日期部分
    media_datetime = MediaCreateDateText[34:53]

    # 解析时间字符串为 datetime 对象
    time_obj = datetime.strptime(media_datetime, "%Y:%m:%d %H:%M:%S")

    # 假设这是 UTC 时间，转换为本地时间
    utc_time = pytz.utc.localize(time_obj)
    local_tz = pytz.timezone("Europe/London")  # 你可以根据需要更改时区
    local_time = utc_time.astimezone(local_tz)

    # 返回 YYYY-MM-DD 格式的字符串，如 2019-11-06
    return local_time

# 使用 exiftool 获取媒体创建日期
def get_metadata(file_path, type):
    if type in [".mp4", ".MP4"]:
        # 先获取 CreateDate
        result_cd = subprocess.run(
            ["exiftool", "-CreateDate", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        create_date = result_cd.stdout if result_cd.returncode == 0 else None

        # 获取 File Modification Date/Time
        result_fmd = subprocess.run(
            ["exiftool", "-FileModifyDate", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        file_modify_date = result_fmd.stdout if result_fmd.returncode == 0 else None

        if create_date and "0000" in create_date:
            return file_modify_date
        return create_date
    elif type in [".JPG", ".jpg"]:
        # 先尝试获取 DateTimeOriginal
        result_dt = subprocess.run(
            ["exiftool", "-DateTimeOriginal", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result_dt.returncode == 0 and result_dt.stdout.strip():
            return result_dt.stdout
        else:
            # 如果 DateTimeOriginal 不存在，尝试获取 CreateDate
            result_cd = subprocess.run(
                ["exiftool", "-CreateDate", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result_cd.returncode == 0:
                return result_cd.stdout
            else:
                print(f"Error: {result_cd.stderr}")
    elif type in [".heic", ".HEIC"]:
        result = subprocess.run(
            ["exiftool", "-CreateDate", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout if result.returncode == 0 else None
    elif type == ".jpeg":
        result = subprocess.run(
            ["exiftool", "-CreateDate", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout if result.returncode == 0 else None

    print(f"Unsupported file type: {type}")
    return None

def process_videos():

    print("欢迎使用本程序！")
    print("软件名称：媒体文件时间校准统一工具（Media File Time Calibrator）\n编写时间：2025年2月28日")
    print("软件版本：1.0.0\n作者GitHub：@caspiankexin\n作者邮箱：mirror_flower@outlook.com")
    print("注意：请做好文件备份，以免丢失!\n版权：免费开源、不得商用!\n如果对您有用，感谢进行打赏!!!\n")
    print("软件功能：\n- 软件可以处理mp4、MP4、jpg、JPG、jpeg、heic格式的文件。\n- 以文件拍摄日期来修改其他时间信息，并重命名。\n- 文件名后加MD5值的前六位，避免时间相同导致文件名冲突。\n- 在重复的文件前加上“重复文件”字样，给予提示。\n- 如需处理其他格式文件，请访问GitHub地址，查看说明。\n")

    folder_path = Path(input("请输入需处理视频的文件夹路径："))

    # 创建一个字典来跟踪每个MD5值的数量
    md5_count = {}

    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            if file_path.suffix in [".mp4", ".jpeg", ".heic", ".jpg", ".JPG", ".MP4", ".HEIC"]:

                MediaCreateDateStr = get_metadata(file_path.resolve(), file_path.suffix)
                if MediaCreateDateStr:
                    if "0000" in MediaCreateDateStr:
                        print('文件' + file_path.name + "媒体创建日期无效")
                        new_filename = "无效日期 " + file_path.name
                        new_path = file_path.parent / new_filename
                        os.rename(file_path, new_path)
                        continue

                    localDate = convertDate(MediaCreateDateStr)

                    # 根据文件类型设置不同的元数据
                    if file_path.suffix in [".mp4", ".MP4"]:
                        subprocess.run(
                            ["exiftool", "-overwrite_original",
                             "-CreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-FileModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-FileCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-ModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-TrackCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-TrackModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-MediaCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-MediaModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), file_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )

                    elif file_path.suffix in [".heic", ".HEIC"]:
                        subprocess.run(
                            ["exiftool", "-overwrite_original",
                             "-FileModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-FileCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-ModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-DateTimeOriginal=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-ProfileDateTime=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), file_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )
                    elif file_path.suffix in [".jpg", ".JPG"]:
                        subprocess.run(
                            ["exiftool", "-overwrite_original",
                             "-FileModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-FileCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-DateTimeOriginal=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-CreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), file_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )

                    elif file_path.suffix == ".jpeg":
                        subprocess.run(
                            ["exiftool", "-overwrite_original",
                             "-FileModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-FileCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                             "-DateTimeOriginal=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), file_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )

                    # 获取日期字符串
                    date_str = localDate.strftime("%Y%m%d%H%M%S")

                    # 计算文件的MD5值
                    md5_hash = hashlib.md5()
                    with open(file_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            md5_hash.update(chunk)
                    md5_code = md5_hash.hexdigest()

                    # 检查该MD5值是否已经存在于字典中
                    if md5_code in md5_count:
                        # 如果存在，则增加序列号
                        md5_count[md5_code] += 1
                        sequence = md5_count[md5_code]
                        new_filename = f"重复文件{sequence}_{date_str}_{md5_code[:6]}{file_path.suffix}"
                    else:
                        # 如果不存在，则将该MD5值添加到字典中，并设置序列号为1
                        md5_count[md5_code] = 1
                        new_filename = f"{date_str}_{md5_code[:6]}{file_path.suffix}"

                    # 重命名文件
                    new_path = file_path.parent / new_filename
                    os.rename(file_path, new_path)
                    print(f"文件 {file_path.name} 已处理完成！")

                else:
                    print('文件' + file_path.name + "媒体创建日期无效")
                    new_filename = "无效日期" + file_path.name
                    new_path = file_path.parent / new_filename
                    os.rename(file_path, new_path)
                    continue

    print("\n" + "文件夹下所有支持的文件，已经全部处理完毕！" + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    process_videos()
    input("\n\n按任意键退出程序...")
