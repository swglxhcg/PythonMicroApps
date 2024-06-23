import os
import subprocess
from pathlib import Path
import sys

def process_video(mp4_file_path):
    # 获取MP4文件的目录和文件名
    file_dir = os.path.dirname(mp4_file_path)
    file_name = os.path.splitext(os.path.basename(mp4_file_path))[0]

    # 设置输出SRT文件的路径
    srt_file_path = os.path.join(file_dir, f"{file_name}.srt")

    # 使用whisper的medium模型处理视频并导出SRT文件
    # command = f"whisper {mp4_file_path} --temperature 0.5 --model medium --output_format srt > {srt_file_path}"
    command = f"whisper \"{mp4_file_path}\" --model medium --language Chinese --output_format srt"
    #print(command)
    subprocess.run(command, shell=True, check=True)

    copy_cmd=f"copy \"{file_name}.srt\" \"{srt_file_path}\""
    subprocess.run(copy_cmd, shell=True, check=True)

def process_from_dir(dir_path):
    mp4_file_path_list =[]
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".mp4"):
            file_base_name = os.path.splitext(os.path.basename(file_name))[0]
            if os.path.exists(os.path.join(dir_path, f"{file_base_name}.srt")):
                print(f"[ChZT信息] \"{file_base_name}.srt\" 已存在，跳过处理 \"{file_name}\"")
            else:
                print(f"[ChZT信息] 加入处理列表 \"{file_name}\"")
                mp4_file_path_list.append(os.path.join(dir_path, file_name))
    print("")
    i=0
    print("[ChZT信息] 文件列表预览")
    for mp4_file_path in mp4_file_path_list:
        print(f"[ChZT信息] [文件{i}] \"{mp4_file_path}\"")
        i=i+1

    confirm = input("[ChZT确认] 请确认操作（输入Y或N，默认Y）：")
    if confirm.lower() == 'y' or confirm=="":
        print("[ChZT信息] 操作已确认, 开始处理")
        for mp4_file_path in mp4_file_path_list:
            
            print(f"[处理中] \"{mp4_file_path}\"")
            process_video(mp4_file_path)
    else:
        print("[ChZT信息] 操作已取消")
    

if __name__ == "__main__":
    # 判断命令行参数
    if len(sys.argv) != 2:
        # 参数错误则输出帮助信息
        print("[ChZT信息] 用法: python script.py <MP4 文件路径>")
        sys.exit(1)
    # path存储参数内容
    path = sys.argv[1]
    # 判断路径参数类型
    if not os.path.exists(path):
        print("[ChZT信息] 路径不存在")
    elif os.path.isfile(path):
        print("[ChZT信息] 这个是文件")
        mp4_file_path=path
        print(f"[ChZT信息] 正在处理 \"{mp4_file_path}\"")
        process_video(mp4_file_path)
    elif os.path.isdir(path):
        print("[ChZT信息] 这个是目录, 读取内容")
        process_from_dir(path)
    else:
        print("[ChZT信息] 这个不知道是什么")

    

