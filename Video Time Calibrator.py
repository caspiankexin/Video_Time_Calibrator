'''
代码名称：视频时间校准统一工具（Video Time Calibrator）
编写日期：2025年2月28日
作者：github（@caspiankexin）
版本：第1版
注意：此代码仅供交流学习，不得作为其他用途。
'''

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
    local_tz = pytz.timezone("Asia/Shanghai")  # 你可以根据需要更改时区
    local_time = utc_time.astimezone(local_tz)

    # 返回 YYYY-MM-DD 格式的字符串，如 2019-11-06
    return local_time

# 使用 exiftool 获取媒体创建日期
def get_metadata(file_path, type):
    arg1 = ""
    if type == ".mp4":
        arg1 = "-CreateDate"

    result = subprocess.run(
        ["exiftool", arg1, file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout
    else:
        print(f"Error: {result.stderr}")

def process_videos():

    print("欢迎使用本程序！")
    print("软件名称：视频时间校准统一工具（Name: Video Time Calibrator）\n编写时间：2025年2月28日")
    print("软件版本：1.0.0\n作者GitHub：@caspiankexin\n作者邮箱：mirror_flower @ outlook.com")
    print("注意：请做好文件备份，以免丢失!\n版权：免费开源、不得商用!\n如果对您有用，感谢进行打赏!!!\n\n")


    folder_path = Path(input("请输入需处理视频的文件夹路径："))
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            if file_path.suffix in [".mp4"]:

                MediaCreateDateStr = get_metadata(file_path.resolve(), file_path.suffix)
                if MediaCreateDateStr:
                    if "0000" in MediaCreateDateStr:
                        print('文件' + file_path.name + "媒体创建日期无效")
                        new_filename = "无效日期 " + file_path.name
                        new_path = file_path.parent / new_filename
                        os.rename(file_path, new_path)
                        continue

                    localDate = convertDate(MediaCreateDateStr)

                    # 使用 exiftool 将 CreateDate 写入到 File Modification Date/Time 和 File Creation Date/Time 以及 File Access Date/Time 以及所有的时间元素里面
                    subprocess.run(
                        ["exiftool", "-overwrite_original",
                         "-FileModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                         "-FileCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                         "-ModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                         "-TrackCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                         "-TrackModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                         "-MediaCreateDate =" + localDate.strftime("%Y:%m:%d %H:%M:%S"),
                         "-MediaModifyDate =" + localDate.strftime("%Y:%m:%d %H:%M:%S"), file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    # 重命名文件
                    new_filename = localDate.strftime("%Y%m%d") + "_" + file_path.name
                    new_path = file_path.parent / new_filename
                    os.rename(file_path, new_path)
                    print(f"文件 {file_path.name} 已处理完成！")

                else:
                    print("该文件没有找到媒体创建日期：" + file_path.name)
    print("\n" + "文件夹下所有mp4文件，已经全部处理完毕！" + "\n")

def show_image_window():
    # 创建一个新的Toplevel窗口
    image_window = tk.Toplevel(root)
    image_window.title("赞赏码")
    image_window.attributes("-topmost", True)  # 设置窗口为最上层

    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 设置弹窗尺寸为屏幕的30%
    window_width = int(screen_width * 0.3)
    window_height = int(screen_height * 0.45)

    # 计算弹窗位置，使其居中显示
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # 设置弹窗尺寸和位置
    image_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 加载PNG图片
    image = Image.open(get_resource_path('images/赞赏码.png'))
    image = image.resize((300, 300), Image.LANCZOS)  # 调整图片大小
    photo = ImageTk.PhotoImage(image)

    # 创建一个Label组件来显示图片
    image_label = tk.Label(image_window, image=photo)
    image_label.image = photo  # 保持对图片的引用
    image_label.pack(pady=10)

    # 创建一个Label组件来显示文字
    text_label = tk.Label(image_window, text="如果对您有用，感谢进行打赏。", font=('Helvetica', 12))
    text_label.pack(pady=10)

def get_resource_path(relative_path):
    # 用于打包含有图片的Python程序
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    show_image_window()
    process_videos()
    input("\n\n按任意键退出程序...")
