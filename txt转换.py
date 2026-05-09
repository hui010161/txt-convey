#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能：
  1. 自动识别 TXT 文档编码（基于 chardet）
  2. 去除文档中的空白行（仅含空格/制表符等空白字符的行）
  3. 将文档编码转为 ANSI（默认 GBK）
  4. Unicode 独有或无法正常转换的字符一律用 “?” 代替
  5. 最大程度保持原文档与转换文档的相似度（保留原始换行符等）
  6. 直接调用 process_txt_folder() 函数处理整个文件夹

依赖：pip install chardet
"""

import os
from pathlib import Path

try:
    import chardet
except ImportError:
    raise ImportError("缺少必要库 chardet，请执行：pip install chardet")


def process_txt_file(file_path, target_encoding='gbk', remove_empty=True):
    """
    处理单个 TXT 文件：检测编码 -> 解码 -> 去除空行 -> 转目标编码 -> 写回
    """
    file_path = Path(file_path)

    # 读取原始字节
    with open(file_path, 'rb') as f:
        raw_bytes = f.read()

    if not raw_bytes:
        print(f"[跳过] 空文件: {file_path}")
        return True

    # 自动识别编码
    detected = chardet.detect(raw_bytes)
    encoding = detected.get('encoding')
    confidence = detected.get('confidence', 0)

    # 置信度过低或未识别时，尝试常见编码
    if encoding is None or confidence < 0.5:
        for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
            try:
                raw_bytes.decode(enc)
                encoding = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            encoding = 'utf-8'  # 最终回退

    print(f"[处理] {file_path}")
    print(f"       检测编码: {encoding} (置信度: {confidence:.2%})")

    # 解码为字符串 (无法解码的字节用替换符 U+FFFD)
    text = raw_bytes.decode(encoding, errors='replace')

    # 去除空白行 (保留原始换行符)
    if remove_empty:
        lines = text.splitlines(keepends=True)
        filtered_lines = [line for line in lines if line.strip()]
        text = ''.join(filtered_lines)

    # 编码为目标编码 (无法表示的字符用 ? 替换)
    new_bytes = text.encode(target_encoding, errors='replace')

    # 写回文件 (二进制模式，保留换行符原样)
    with open(file_path, 'wb') as f:
        f.write(new_bytes)

    print(f"       转换完成 -> {file_path}")
    return True


def process_txt_folder(folder_path,
                       ext='.txt',
                       recursive=False,
                       target_encoding='gbk',
                       remove_empty=True):
    """
    处理文件夹中所有指定扩展名的 TXT 文件。

    参数：
        folder_path     : 目标文件夹路径 (str 或 Path)
        ext             : 文件扩展名，默认 '.txt'
        recursive       : 是否递归处理子文件夹，默认 False
        target_encoding : 目标 ANSI 编码，默认 'gbk'
        remove_empty    : 是否去除空白行，默认 True
    """
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"路径不存在或不是文件夹: {folder}")

    # 保证扩展名以点开头
    if not ext.startswith('.'):
        ext = '.' + ext

    # 收集文件
    if recursive:
        files = list(folder.rglob(f'*{ext}'))
    else:
        files = list(folder.glob(f'*{ext}'))

    if not files:
        print(f"在 '{folder}' 中没有找到 *{ext} 文件。")
        return

    print(f"找到 {len(files)} 个文件，开始处理...\n")

    success_count = 0
    for fp in files:
        try:
            if process_txt_file(fp, target_encoding, remove_empty):
                success_count += 1
        except Exception as e:
            print(f"[错误] 处理失败 {fp}: {e}")

    print(f"\n处理完成：成功 {success_count}/{len(files)} 个文件。")


# ---------- 使用示例 ----------
if __name__ == '__main__':
    # 请修改为你的实际文件夹路径
    target_folder = r"C:\Users\w1800\Downloads\新建文件夹"   # 替换成你的文件夹

    # 直接调用函数，无需命令行
    process_txt_folder(
        folder_path=target_folder,
        ext='.txt',          # 处理 .txt 文件
        recursive=True,      # 包含子文件夹
        target_encoding='gbk',
        remove_empty=True
    )
