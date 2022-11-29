import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm


all_subjects = ['Toán', 'Văn', 'Ngoại ngữ', 'Lí', 'Hóa', 'Sinh', 'Sử', 'Địa', 'GDCD'] # Vietnamese names of the subjects
# English names: ['Maths', 'Literature', 'Foreign_Language', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Civic_Education']
cluster = '01' # there are 63 clusters from 01 to 64 (except 20)
cluster_data = [] # to store all the students' scores in that cluster
patience = 0 # if we can't find the ID's infomation after a large enough number of times, we assume that all of the cluster's data have been taken

for student in tqdm(range(1, 30001), ascii=True):

	# Get the student ID
	student_str = str(student)
	ID = cluster + '0' * ( 6 - len(student_str) ) + student_str
	# The ID is in the form of xxyyyyyy, where xx is the cluster and yyyyyy is the numerical order.

	# Input the ID to the web and check if that ID exists
	url = f'https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2022/{ID}.html'
	response = requests.get(url)
	if response.status_code != 200: # the ID not exist!'
		patience += 1
		if patience == 500: # after 500 times not getting data, we terminate the process
			break
		continue

	# If the ID exists, then get the scores with BeautifulSoup
	student_scores = [-1] * len(all_subjects) # -1 means that the student doesn't get the score of that subject
	soup = BeautifulSoup(response.content, 'html.parser')
	table_body = soup.find('tbody') 
	# The scores are displayed in a two-column table. The left one contains the subjects while the right one contains the scores

	for row in table_body.find_all('tr'):
		cols = row.find_all('td')
		subject = cols[0].get_text()
		score = float(cols[1].get_text())

		position_of_subject = all_subjects.index(subject)
		student_scores[position_of_subject] = score # update the score

	cluster_data.append([ID] + student_scores) # add that student's scores to the data store

	if student % 500 == 0: # save after some iterations 
		header = ['ID', 'Maths', 'Literature', 'Foreign_Language', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Civic_Education']
		df = pd.DataFrame(cluster_data, columns=header)
		path = f'data/Cluster_{cluster}.csv'

		if os.path.isfile(path):
			df.to_csv(path, mode='a', header=False, index=False)
		else:
			df.to_csv(path, index=False)
		cluster_data.clear()



# Save to a csv file

# header = ['ID', 'Maths', 'Literature', 'Foreign_Language', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Civic_Education']
# df = pd.DataFrame(cluster_data, columns=header)
# path = f'data/Cluster_{cluster}.csv'

# if os.path.isfile(path):
# 	df.to_csv(path, mode='a', header=False, index=False)
# else:
# 	df.to_csv(path, index=False)


