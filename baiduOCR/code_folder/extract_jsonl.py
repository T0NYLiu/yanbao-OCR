import json

# 文件路径
jsonl_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/train_v2.jsonl'
output_jsonl_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/train_v3.jsonl'

# 字典用于记录最后一次出现的image字段的数据
image_to_message = {}

# 读取JSONL文件并逐行处理
with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
    for line in jsonl_file:
        try:
            # 解析JSONL中的每一行
            message = json.loads(line.strip())
            # 获取image字段
            image_path = message['messages'][0].get('image', '')
            # 使用字典存储最后一次出现的image对应的数据
            image_to_message[image_path] = message
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

# 将最后一次出现的每个image的JSON数据写入输出文件
with open(output_jsonl_path, 'w', encoding='utf-8') as output_file:
    for message in image_to_message.values():
        output_file.write(json.dumps(message, ensure_ascii=False) + '\n')

# 输出有多少条数据
print(f"最终保存的条数为: {len(image_to_message)}")
