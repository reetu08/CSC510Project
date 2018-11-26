from pydriller import RepositoryMining
import datetime

#function to write a string at the end of a file
def writeInFile(fileD, strData):
  fileToWrite = open( fileD, 'a', encoding='utf-8')
  fileToWrite.seek(0,2)
  fileToWrite.write(strData)
  fileToWrite.close()

#reading commits between a specific timeframe
dt1 = datetime.datetime(2018, 6, 1, 17, 0, 0)
dt2 = datetime.datetime(2018, 10, 1, 17, 0, 0)

#writing the extracted data to a file
write_file='C:/pydriller/resources/Puppet_all_files_author_commit.csv'
#write_file='C:/pydriller/resources/GitLab_all_files_author_commit.csv'
repo_address='../test-repos/puppet/'
#repo_address='../test-repos/gitlabhq/'
header = 'author_name,file_name\n'
writeInFile(write_file,header)

#extracting commits in the timeframe between dt1 to dt2 
#reading the commit authors name and the names of changed files 
for commit in RepositoryMining(repo_address,since=dt1, to=dt2).traverse_commits():
    #print('Hash {} Author {} modified the files'.format(commit.hash, commit.author.name))
    for mod in commit.modifications:
        row = '{author},{file}\n'.format(author=commit.author.name, file=mod.filename)
        writeInFile(write_file,row)
        print (row)
    