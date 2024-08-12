import Levenshtein
import re

# 文件路径
baidu_ocr_output_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/baidu_ocr.txt'
baidu_4o_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/4o.txt'
output_similarity_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/output_similarity.txt'
error_log_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/error_log.txt'
similarity_distribution_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/similarity_distribution.txt'
difference_characters_path = r'/data/zhaoshuofeng/workplace/hongan_data/研报+OCR/baiduOCR/data_folder/difference_characters.txt'

# 计算编辑距离和相似度
def calculate_distance_similarity(paddle_str, origin_str):
    distance = Levenshtein.distance(paddle_str, origin_str)
    similarity = 1 - (distance / max(len(paddle_str), len(origin_str)))
    return similarity, distance

# 计算不同字符
def get_diff_characters(paddle_str, origin_str):
    diff = Levenshtein.editops(paddle_str, origin_str)
    diff_chars = []
    for op, i, j in diff:
        if op == 'replace':
            diff_chars.append((paddle_str[i], origin_str[j]))
        elif op == 'delete':
            diff_chars.append((paddle_str[i], ''))
        elif op == 'insert':
            diff_chars.append(('', origin_str[j]))
    return diff_chars

# 移动窗口，找到与OCR字符块最匹配的子字符串
def find_best_match(block, content):
    max_similarity = 0
    best_match = ""
    best_distance = float('inf')
    block_len = len(block)
    
    for i in range(len(content) - block_len + 1):
        window = content[i:i + block_len]
        similarity, distance = calculate_distance_similarity(block, window)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = window
            best_distance = distance
            
    return best_match, max_similarity, best_distance

paddle_file_content_map = {}
baidu_4o_file_content_map = {}
pattern = re.compile(r'文件名：(.*?) 图片内容：(.*)')
extension_pattern = re.compile(r'\.jpg|\.jpeg|\.png$', re.IGNORECASE)

# 读取 Baidu OCR 输出文件
with open(baidu_ocr_output_path, 'r', encoding='utf-8') as baidu_f:
    for line in baidu_f:
        match = pattern.match(line)
        if match:
            filename, content = match.groups()
            filename = re.sub(extension_pattern, '', filename)
            try:
                content_list = eval(content)  # 将字符串转换为列表
                paddle_file_content_map[filename] = content_list
            except:
                print(f"内容不是有效的列表：{content}")

# 读取4o 输出文件
with open(baidu_4o_path, 'r', encoding='utf-8') as baidu_4o_f:
    for line in baidu_4o_f:
        match = pattern.match(line)
        if match:
            filename, content = match.groups()
            baidu_4o_file_content_map[filename] = content

# 初始化分布数据结构
similarity_distribution = {
    '0-30': {'count': 0, 'char_diff': {}},
    '30-35': {'count': 0, 'char_diff': {}},
    '35-40': {'count': 0, 'char_diff': {}},
    '40-45': {'count': 0, 'char_diff': {}},
    '45-50': {'count': 0, 'char_diff': {}},
    '50-55': {'count': 0, 'char_diff': {}},
    '55-60': {'count': 0, 'char_diff': {}},
    '60-65': {'count': 0, 'char_diff': {}},
    '65-70': {'count': 0, 'char_diff': {}},
    '70-75': {'count': 0, 'char_diff': {}},
    '75-80': {'count': 0, 'char_diff': {}},
    '80-85': {'count': 0, 'char_diff': {}},
    '85-90': {'count': 0, 'char_diff': {}},
    '90-95': {'count': 0, 'char_diff': {}},
    '95-100': {'count': 0, 'char_diff': {}},
}

with open(error_log_path, 'w', encoding='utf-8') as error_log_f, open(output_similarity_path, 'w', encoding='utf-8') as similarity_output_f, open(difference_characters_path, 'w', encoding='utf-8') as diff_chars_output_f:
    for filename in paddle_file_content_map:
        if filename in baidu_4o_file_content_map:
            paddle_contents = paddle_file_content_map[filename]
            yanbao_ocr_content = baidu_4o_file_content_map[filename]

            total_similarity = 0
            block_count = 0

            for block in paddle_contents:
                best_match, max_similarity, best_distance = find_best_match(block, yanbao_ocr_content)
                total_similarity += max_similarity
                block_count += 1

                if best_distance > 0:    
                    similarity_output_f.write(f"文件名：{filename} 文本块：{block} 匹配子串：{best_match} 相似度：{max_similarity:.4f} 编辑距离：{best_distance}\n")

                diff_chars = get_diff_characters(block, best_match)
                if diff_chars:
                    diff_chars_output_f.write(f"文件名：{filename} 文本块：{block} 匹配子串：{best_match} 差异字符：{diff_chars}\n")

            # 计算整体相似度
            if block_count > 0:
                overall_similarity = total_similarity / block_count
                if 0 <= overall_similarity < 0.3:
                    key = '0-30'
                elif 0.3 <= overall_similarity < 0.35:
                    key = '30-35'
                elif 0.35 <= overall_similarity < 0.4:
                    key = '35-40'
                elif 0.4 <= overall_similarity < 0.45:
                    key = '40-45'
                elif 0.45 <= overall_similarity < 0.5:
                    key = '45-50'
                elif 0.5 <= overall_similarity <= 0.55:
                    key = '50-55'
                elif 0.55 <= overall_similarity <= 0.6:
                    key = '55-60'
                elif 0.6 <= overall_similarity <= 0.65:
                    key = '60-65'
                elif 0.65 <= overall_similarity <= 0.7:
                    key = '65-70'
                elif 0.7 <= overall_similarity <= 0.75:
                    key = '70-75'
                elif 0.75 <= overall_similarity <= 0.8:
                    key = '75-80'
                elif 0.8 <= overall_similarity <= 0.85:
                    key = '80-85'
                elif 0.85 <= overall_similarity <= 0.9:
                    key = '85-90'
                elif 0.9 <= overall_similarity <= 0.95:
                    key = '90-95'
                elif 0.95 <= overall_similarity <= 1:
                    key = '95-100'
                else:
                    key = None

                if key:
                    similarity_distribution[key]['count'] += 1
                    char_diff = best_distance
                    if char_diff not in similarity_distribution[key]['char_diff']:
                        similarity_distribution[key]['char_diff'][char_diff] = 0
                    similarity_distribution[key]['char_diff'][char_diff] += 1

            else:
                overall_similarity = 0

            similarity_output_f.write(f"文件名：{filename} 整体相似度：{overall_similarity:.4f}\n")

        else:
            error_log_f.write(f"文件名：{filename} 在研报 OCR 结果中未找到。\n")

# 输出相似度分布
with open(similarity_distribution_path, 'w', encoding='utf-8') as dist_output_f:
    for key, value in similarity_distribution.items():
        dist_output_f.write(f"{key}%: {value['count']}句\n")
        for char_diff, count in value['char_diff'].items():
            dist_output_f.write(f"    {char_diff}字差异: {count}句\n")

print(f"OCR 处理完成，结果已保存到 {output_similarity_path}")
print(f"错误日志已保存到 {error_log_path}")
print(f"相似度分布已保存到 {similarity_distribution_path}")