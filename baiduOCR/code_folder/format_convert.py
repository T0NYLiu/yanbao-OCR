import json

# 输入和输出文件路径
input_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/baidu_ocr.jsonl'
output_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/baidu_ocr.txt'

# 打开输入JSON文件
with open(input_file_path, 'r', encoding='utf-8') as input_file:
    # 打开输出文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # 逐行读取输入文件
        for line in input_file:
            # 解析JSON数据
            data = json.loads(line.strip())

            # 获取文件名和OCR识别的结果
            filename = data.get('filename')
            words_result = data.get('result', {}).get('words_result', [])

            # 将OCR结果转换为列表格式
            text_blocks = [entry['words'] for entry in words_result]

            # 将数据转换为指定的格式
            output_line = f"文件名：{filename} 图片内容：{text_blocks}\n"

            # 将转换后的数据写入输出文件
            output_file.write(output_line)

print("转换完成，结果已保存到", output_file_path)
