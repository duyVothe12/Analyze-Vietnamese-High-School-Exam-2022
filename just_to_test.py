import pandas as pd
import requests
from bs4 import BeautifulSoup

# info = []
# for cluster in range(1, 80):
# 	cluster_str = '0' * (2 - len(str(cluster))) + str(cluster)
# 	url = f'https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2022/{cluster_str}000001.html'
# 	response = requests.get(url)
# 	if response.status_code != 200:
# 		print(f'{cluster_str} not exist!')
# 		continue

# 	soup = BeautifulSoup(response.content, 'html.parser')
# 	edu = soup.find("p", class_= "edu-institution")
# 	st = edu.get_text()
# 	st = st.replace('Sở GD&ĐT ', '')
# 	st = st.replace('Tỉnh ', '')
# 	st = st.replace('Thành Phố ', '')

# 	info.append([cluster_str, st])


# print(info)


# for cl in range(1, 10):
# 	cl_str = str(cl)
# 	file = f'data/Cluster_0{cl}.csv'
# 	df = pd.read_csv(file, dtype={'ID':str})
# 	print(cl, df['ID'].is_unique)


f1 = [f'data/Cluster_0{cl}.csv' for cl in range(1, 10)]
f2 = [f'data/Cluster_{cl}.csv' for cl in range(10, 20)]
f3 = [f'data/Cluster_{cl}.csv' for cl in range(21, 65)]
fa = f1 + f2 + f3

dfs = [pd.read_csv(f, dtype={'ID':str}) for f in fa]
df = pd.concat(dfs, ignore_index=True)
df.to_csv('data/all_data.csv', index=False)
finalID = df['ID'].iloc[-1] # get last element of a dataframe column
