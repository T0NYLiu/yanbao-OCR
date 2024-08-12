import json
import os

i = 0
# 文件路径
jsonl_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/train.jsonl'
txt_file_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/high_similarity_filenames.txt'
output_jsonl_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/train_v2.jsonl'

# 读取TXT文件中的所有文件名
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    filenames = [line.strip() for line in txt_file]
    print(filenames)

# 打开JSONL文件并逐行筛选
with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file, open(output_jsonl_path, 'w', encoding='utf-8') as output_file:
    for line in jsonl_file:
        try:
            # 解析JSONL中的每一行
            message = json.loads(line.strip())
            # 检查是否包含TXT文件里的文件名
            image_path = message['messages'][0].get('image','')
            # 提取出文件名部分（带扩展名）
            img_name_with_extension = os.path.basename(image_path)
            # 去除扩展名
            img_name = os.path.splitext(img_name_with_extension)[0]
            print(img_name)
            # print(image_path)
            if any(filename == img_name for filename in filenames):
                # 将符合条件的JSON行写入输出文件
                output_file.write(json.dumps(message, ensure_ascii=False) + '\n')
                i+=1
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

print(f"筛选后的数据已保存到 {output_jsonl_path},筛选了{i}份数据")
