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
from tkinter import filedialog, scrolledtext
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


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
    folder_path = Path(folder_path_var.get())
    log_text.delete(1.0, tk.END)
    log_text.insert(tk.END, "开始遍历文件夹...\n")
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            if file_path.suffix in [".mp4"]:

                MediaCreateDateStr = get_metadata(file_path.resolve(), file_path.suffix)
                if MediaCreateDateStr:
                    if "0000" in MediaCreateDateStr:
                        log_text.insert(tk.END, '文件' + file_path.name + "媒体创建日期无效" + "\n")
                        new_filename = "无效日期 " + file_path.name
                        new_path = file_path.parent / new_filename
                        os.rename(file_path, new_path)
                        continue

                    localDate = convertDate(MediaCreateDateStr)

                    # 使用 exiftool 将 CreateDate 写入到 File Modification Date/Time 和 File Creation Date/Time 和 File Access Date/Time 以及所有的时间元素里面
                    subprocess.run(
                        ["exiftool", "-overwrite_original", "-FileModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), "-FileCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), "-ModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), "-TrackCreateDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), "-TrackModifyDate=" + localDate.strftime("%Y:%m:%d %H:%M:%S"), "-MediaCreateDate =" + localDate.strftime("%Y:%m:%d %H:%M:%S"), "-MediaModifyDate =" + localDate.strftime("%Y:%m:%d %H:%M:%S"), file_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    # 重命名文件
                    new_filename = localDate.strftime("%Y%m%d") + "_" + file_path.name
                    new_path = file_path.parent / new_filename
                    os.rename(file_path, new_path)
                    log_text.insert(tk.END, f"文件 {file_path.name} 已重命名为 {new_filename}\n")

                else:
                    log_text.insert(tk.END, "该文件没有找到媒体创建日期：" + file_path.name + "\n")
    log_text.insert(tk.END, "\n" + "文件夹下所有mp4文件，已经全部处理完毕！" + "\n" + "文件夹下所有mp4文件，已经全部处理完毕！" + "\n" + "文件夹下所有mp4文件，已经全部处理完毕！" + "\n")



def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)

# 创建主窗口
root = tk.Tk()
root.title("视频时间校准统一工具（Video Time Calibrator）")


# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置窗口尺寸为屏幕的60%
window_width = int(screen_width * 0.6)
window_height = int(screen_height * 0.6)

# 计算窗口位置，使其居中显示
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# 设置窗口尺寸和位置
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 修改布局，使软件信息区域在右侧
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# 文件夹路径输入区域
folder_path_var = tk.StringVar()
folder_path_entry = tk.Entry(root, textvariable=folder_path_var, width=50)
folder_path_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
browse_button = tk.Button(root, text="浏览", command=browse_folder, font=('Helvetica', 12))
browse_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

# 程序运行状态显示区域
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=28)
log_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
log_text.configure(yscrollcommand=True)

# 软件信息介绍区域
info_label = tk.Label(root, text="软件名称：视频时间校准统一工具\n\nName: Video Time Calibrator\n\n软件版本：1.0.0\n\n作者GitHub：@caspiankexin\n\n作者邮箱：mirror_flower@outlook.com\n\n编写时间：2025年2月28日\n\n注意：请做好文件备份，以免丢失\n\n版权：免费开源、不得商用\n\n如果对您有用，感谢进行打赏!", font=('Helvetica', 11), anchor='w')
info_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky='nsew')


# 开始按钮
start_button = tk.Button(root, text="开始处理", command=process_videos, font=('Helvetica', 12))
start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

root.mainloop()
