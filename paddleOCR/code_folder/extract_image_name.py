import re

# 定义文件路径
input_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/data_folder/paddle_ocr_output.txt'
output_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/data_folder/processed_name.txt'

# 定义正则表达式模式
pattern = re.compile(r'文件名：(.+?) 图片内容：')

# 存储提取到的文件名
file_names = []

# 读取输入文件并提取文件名
with open(input_file_path, 'r', encoding='utf-8') as infile:
    for line in infile:
        match = pattern.search(line)
        if match:
            file_name = match.group(1)
            file_names.append(file_name)

# 将提取到的文件名写入输出文件
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for file_name in file_names:
        outfile.write(file_name + '\n')

print(f"提取完成，结果已保存到 {output_file_path}")
