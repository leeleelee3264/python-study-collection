import re
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

from konlpy.tag import Hannanum
from apyori import apriori

# 망했음 실행이 안됨

# Korea NLP
korean_nlp = Hannanum()
my_min_support = 0.01

# 파일 읽기
f = open('vts_message.txt', 'r', encoding='UTF-8')
lines = f.readlines()
f.close()


# text parsing
data_set = []
for i in range(len(lines)):
    data_set.append(korean_nlp.nouns(re.sub('[^가-힣a-zA-Z\s]', '', lines[i])))

# f = open('vts_parsed_message.txt', 'w', encoding='UTF-8')
# for i in range(len(data_set)):
#     str_mode = ','.join(data_set[i])
#     f.write(str_mode, )

print('파싱은 끝났음')

start_time = time.time()

# 데이터 정형화
result = (list(apriori(data_set, min_support=my_min_support)))
df = pd.DataFrame(result)
df['length'] = df['items'].apply(lambda x: len(x))
df = df[(df['length'] == 2) &
        (df['support'] >= my_min_support)].sort_values(by='support', ascending=False)

df.head(10)
print(f'알고리즘 적용 수행 시간: {time.time() - start_time}')

# networkx 그래프 정의
G = nx.Graph()
ar = (df['items'])
G.add_edges_from(ar)

pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))

# 그래프 그리기

print('그래프 그리기 시작!')
pos = nx.planar_layout(G)
plt.figure(figsize=(16,12)); plt.axis('off')
nx.draw_networkx(G, font_family='KoPubDotum', font_size=16,
                 pos=pos, node_color=list(pr.values()), node_size=nsize,
                 alpha=0.7, edge_color='.5', cmap=plt.cm.YIGn)
plt.savefig('img.png', bbox_inches='tight')

print('진짜 다 끝남')

