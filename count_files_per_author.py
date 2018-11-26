import pandas as pd
import numpy as np

def writeInFile(fileD, strData):
  fileToWrite = open( fileD, 'w')
  fileToWrite.seek(0,2)
  fileToWrite.write(strData)
  fileToWrite.close()

#read_file is the file from which we are reading the author names and file names
read_file   ='C:/pydriller/resources/Puppet_all_files_author_commit.csv'
#read_file   ='C:/pydriller/resources/GitLab_all_files_author_commit.csv'
read_df     = pd.read_csv(read_file,usecols=[0,1])
#write_file is where we will store the extracted data
write_file  ='C:/pydriller/resources/Puppet_all_files_count_per_author.csv'
#write_file  ='C:/pydriller/resources/GitLab_all_files_count_per_author.csv'
#second_df    = pd.read_csv(write_file)
write2 = 'C:/pydriller/resources/Puppet_minor_contribution.csv'
#write2 = 'C:/pydriller/resources/GitLab_minor_contribution.csv'

#finding the unique filenames from the list
file_list= np.array(read_df['file_name'])
header= np.unique(file_list)
#header=','.join(np.unique(file_list))
#header= 'author_name,'+header+'\n'
#writeInFile(write_file,header) 

#finding the unique author names from the list and 
#creating a dataframe with author names in rows and filenames in column
authors= np.array(read_df['author_name'])
author_list=np.unique(authors)
matrix = pd.DataFrame(index=author_list,columns=header)
matrix =matrix.fillna(0)

#counting the frequency of commits by every author per file
for index, row in read_df.iterrows():
    matrix.at[row['author_name'],row['file_name']] +=1

#calculating total number of commits per file
matrix.loc['Total']= matrix.sum()
matrix.to_csv(write_file)
my='less','total'
minor = pd.DataFrame(index=my,columns=header)
                
#calculating the minor contribution ratio per author per file        
for column in matrix.columns:
    count =0
    author=0
    for index,row in matrix.iterrows():
        if index!='Total':
            row = row/matrix.loc['Total']
            if row[column]*100>0 and row[column]*100<5:
                count+=1
                author+=1
                print ('*********Minor contribution {ratio}% by {author} On the file {filename}'.format(ratio=row[column]*100,author=index,filename=column))
            elif row[column]*100>5:
                author+=1
                #print ('/////////Major contribution {ratio}% by {author}'.format(ratio=row[column]*100,author=index))
    minor.loc['less'][column]=count
    minor.loc['total'][column]=author

minor.to_csv(write2)