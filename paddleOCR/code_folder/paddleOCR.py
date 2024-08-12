import os
from paddleocr import PaddleOCR

# 初始化 PaddleOCR，使用 GPU
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang='ch')

# 输入文件夹和输出文件路径
img_folder = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/yanbao_image/7300'
output_data_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/data_folder/paddle_ocr_output.txt'
processed_files_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/data_folder/processed_name.txt'

# 获取文件列表
img_files = [f for f in os.listdir(img_folder) if os.path.isfile(os.path.join(img_folder, f))]

# 读取已经处理好的文件名
processed_files = set()
if os.path.exists(processed_files_path):
    with open(processed_files_path, 'r', encoding='utf-8') as processed_f:
        for line in processed_f:
            processed_files.add(line.strip())

with open(output_data_path, 'a', encoding='utf-8') as output_f, open(processed_files_path, 'a', encoding='utf-8') as processed_f:
    for img_file in img_files:
        if img_file in processed_files:
            print(f"Skipping already processed file: {img_file}")
            continue

        img_path = os.path.join(img_folder, img_file)

        try:
            # 进行 OCR 处理
            result = ocr.ocr(img_path, cls=True)

            # 提取纯文本
            text_blocks = []
            if result and len(result) > 0 and len(result[0]) > 0:
                text_blocks = [line[1][0] for line in result[0]]
            else:
                full_blocks = ["No text found"]

            output_f.write(f"文件名：{img_file} 图片内容：{text_blocks}\n")
            processed_f.write(f"{img_file}\n")
        except Exception as e:
            print(f"Error processing file {img_file}: {e}")
            output_f.write(f"文件名：{img_file} 图片内容：Error occurred\n")

print(f"OCR 处理完成，结果已保存到 {output_data_path}")
