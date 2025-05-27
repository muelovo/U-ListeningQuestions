from bs4 import BeautifulSoup
from moviepy import AudioFileClip, concatenate_audioclips
import requests
import os
import re

# 设置文件夹名称
folder_path = 'U5'

# 读取 HTML 文件
with open(folder_path + '.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')
spans = soup.find_all('span')

# 过滤掉不含链接的 span
filtered_spans = [span for span in spans if "https" not in span.text]
for span in spans:
    if span in filtered_spans:
        span.decompose()

# 提取 span 中的音频链接
pattern = r'"(.*?)"'
data = [span.text for span in soup.find_all('span') if span.text.strip()]
links = []
for item in data:
    link = re.findall(pattern, item)
    links.extend(link)

# 清理和去重
new_links = [
    i for i in links
    if i != '15' and i != 'https://ucampus.cdn.unipus.cn/uexercise/_zy/sys/common/question_num/question.mp3'
]
new_list = []
for i in new_links:
    if i not in new_list:
        new_list.append(i)

# 文件命名
fileNameList = ['1', '2', '3', '4', '4q1', '4q2', '4q3', '4q4', '5', '5q1', '5q2', '5q3', '5q4',
                '6', '6q1', '6q2', '6q3', '6q4', '7', '7q1', '7q2', '7q3', '7q4', '8']

# 创建音频下载文件夹
os.makedirs(folder_path, exist_ok=True)

# 下载音频文件
for index, url in enumerate(new_list):
    print(f"Downloading: {url}")
    response = requests.get(url)
    filename = f'{folder_path}/{fileNameList[index]}.mp3'
    with open(filename, 'wb') as f:
        f.write(response.content)

# 合并音频（使用 moviepy）
print("Merging audio files...")
audio_clips = []
for name in fileNameList:
    path = f"{folder_path}/{name}.mp3"
    if os.path.exists(path):
        audio_clips.append(AudioFileClip(path))

if audio_clips:
    final_clip = concatenate_audioclips(audio_clips)
    output_path = f"{folder_path}_merged.mp3"
    final_clip.write_audiofile(output_path)
    print(f"✅ 合并完成，输出文件：{output_path}")
else:
    print("⚠️ 没有找到可合并的音频文件。")
