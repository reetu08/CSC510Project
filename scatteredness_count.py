import os
import subprocess
from scipy.stats import entropy
from collections import Counter
import math
import pandas as pd

def getDeveloperScatternessOfFile(param_file_path, repo_path, sloc):
   '''
   output list
   '''
   lineNoProb        = []
   lineNoCnt         = []
   '''
   '''
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print 'inside the function path is',theFile
   theFile=theFile.replace('\\', '/')
   if "'" in theFile:
       return 0.0
   #print 'the path is changed to ',theFile
   blameCommand      = " git blame -n " + theFile + " | awk '{print $2}' "
   command2Run       = cdCommand + blameCommand
   #print 'command2run is ',command2Run
   lineNoProb        = []

   blame_output      = subprocess.check_output(['C:\\cygwin64\\bin\\bash.exe','-c', command2Run])
   blame_output      = blame_output.split('\n')
   blame_output      = [x_ for x_ in blame_output if x_!='']
   line_chng_dict    = dict(Counter(blame_output))
   #print line_chng_dict
   for lineNo in xrange(sloc):
       line_key  = str(lineNo + 1)
       if (line_key in line_chng_dict):
          line_cnt  = line_chng_dict[line_key]
       else:
          line_cnt  = 0
       lineNoCnt.append(line_cnt)   ### Version 2
   scatterness_cnt  = round(entropy(lineNoCnt), 5)  ##Version 2
   '''
   handling -inf, inf, nan
   '''
   if((scatterness_cnt == float("-inf")) or (scatterness_cnt == float("inf")) or (scatterness_cnt == float("nan")) or math.isnan(scatterness_cnt)):
     scatterness_cnt = float(0)
    
   return scatterness_cnt

#rootDir="C:/pydriller/test-repos/puppet"
rootDir="C:/pydriller/test-repos/gitlabhq"
print rootDir
header = ['filename','scatterness']
df = pd.DataFrame(columns=header)
#write_file = 'C:/pydriller/resources/puppet_file_scatterness.csv'
write_file = 'C:/pydriller/resources/GitLab_file_scatterness.csv'

for root, dirs, files in os.walk(rootDir):
    for fileName in files:
        print "fileName : ",fileName
        file_path_p=os.path.join(root,fileName)
        #print file_path_p
        sloc = sum(1 for line in open(file_path_p))
        if (not '.png' in fileName) and (not '.gif' in fileName) and (not '.jpg' in fileName) and (not '.svg' in fileName):
            count= getDeveloperScatternessOfFile(file_path_p,rootDir, sloc)
            print count
            #data=[fileName,count]
            #data=fileName+','+str(count)
            df=df.append({'filename': fileName, 'scatterness': count},ignore_index = True)
print df
df.to_csv(write_file, index=False)