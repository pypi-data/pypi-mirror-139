"""
文件读写。ExcelHandler读写excel。
"""
import os
import shutil
from datetime import datetime


def find_file(start_dir, file_name):
    doc_list = os.listdir(start_dir)
    for doc in doc_list:
        doc_path = os.path.join(start_dir, doc)
        if os.path.isdir(doc_path):
            result = find_file(doc_path, file_name)
            if result:
                return result
        else:
            if doc == file_name:
                return doc_path


def last_file(path):
    """找到最新的文件或文件夹"""
    # 列出目录下所有的文件
    doc_list = os.listdir(path)
    # 对文件修改时间进行升序排列
    doc_list.sort(key=lambda fn: os.path.getmtime(path + '\\' + fn))
    # 获取最新修改时间的文件
    filetime = datetime.fromtimestamp(os.path.getmtime(path + '\\' + doc_list[-1]))
    # 获取文件所在目录
    filepath = os.path.join(path, doc_list[-1])
    print("最新修改的文件(夹)：" + doc_list[-1])
    print("时间：" + filetime.strftime('%Y-%m-%d %H-%M-%S'))
    return filepath


def move_file(old_path, new_path):
    print(old_path)
    print(new_path)
    fileList = os.listdir(old_path)  # 列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    print(fileList)
    for file in fileList:
        if file.startswith('__init__'):
            continue
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        print('src:', src)
        print('dst:', dst)
        shutil.move(src, dst)


def del_file(path):
    """删除指定文件夹的所有文件"""
    ls = os.listdir(path)
    for i in ls:
        if i.startswith('__init__'):
            continue
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            print('delete file:%s' % c_path)
            os.remove(c_path)


