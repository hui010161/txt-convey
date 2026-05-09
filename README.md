# txt-convey
电子书工具
功能：
  1. 自动识别 TXT 文档编码（基于 chardet）
  2. 去除文档中的空白行（仅含空格/制表符等空白字符的行）
  3. 将文档编码转为 ANSI（默认 GBK）
  4. Unicode 独有或无法正常转换的字符一律用 “?” 代替
  5. 最大程度保持原文档与转换文档的相似度（保留原始换行符等）
  6. 直接调用 process_txt_folder() 函数处理整个文件夹

依赖：pip install chardet
