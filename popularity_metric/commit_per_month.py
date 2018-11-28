import pandas as pd
import datetime

def getDurationInSO(end_, start_):

    end_date = end_.split('-')
    end_date = [int(x_) for x_ in end_date]
    sta_date = start_.split('-')
    sta_date = [int(x_) for x_ in sta_date]

    d0 = datetime.date(sta_date[0], sta_date[1], sta_date[2])
    d1 = datetime.date(end_date[0], end_date[1], end_date[2])
    delta_ = d1 - d0
    # print delta_.days
    # return delta_.days
    return delta_.days / 30

def writeInFile(fileD, strData):
  fileToWrite = open( fileD, 'a')
  fileToWrite.write(strData)
  fileToWrite.close()

tr_file   = 'commit_count.csv'

tr_df        = pd.read_csv(tr_file, usecols=[0, 1, 2, 3])
matched_df   = pd.DataFrame()
data = []


for index, row in tr_df.iterrows():
    month = getDurationInSO(row['latest_commit_date'],row['first_commit_date'])
    print row['repo_name'], month, row['total_commit_count']
    # average commit per month>=2
    if month>0:
      avg_commit=float(row['total_commit_count'])/float(month)
      if avg_commit>1:
        print avg_commit
        matched_df = matched_df.append(tr_df[tr_df.repo_name == row['repo_name']],ignore_index=True)

#print matched_df
df.to_csv(tr_file, index=False)