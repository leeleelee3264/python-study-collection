from wordcloud import WordCloud
from PIL import Image
import numpy as np

text = ''
with open("text_sample2.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[5:]:
        if '] [' in line:
            text += line.split('] ')[2].replace('저는', '').replace('저도', '').replace('ㅋ', '').replace('ㅠ', '').replace('이모티콘\n', '').replace('사진\n', '').replace('삭제된 메시지입니다', '' )
print(text)

# wc = WordCloud(font_path='C:\\Windows\\Fonts\\YBLA05.TTF', background_color="white", width=600, height=400)
# wc.generate(text)
# wc.to_file("result.png")


mask = np.array(Image.open('rect.png'))
wc = WordCloud(font_path='C:\\Windows\\Fonts\\YBLA05.TTF', background_color="white", mask=mask)
wc.generate(text)
wc.to_file("result_masked.png")