import os
import subprocess
from scipy.stats import entropy
def getDeveloperScatternessOfFile(param_file_path, repo_path, sloc):
   '''
   output list
   '''
   lineNoProb        = []
   lineNoCnt         = []
   '''
   '''
   cdCommand         = "cd " + repo_path + " ; "
   print "inside the function i found the repopath ",repo_path
   theFile           = param_file_path
   #theFile           = os.path.relpath(param_file_path, repo_path)
   print "inside the function i found the filepath ",theFile
   
   blameCommand      = " git blame -n " + theFile + " | awk '{print $2}' "
   command2Run       = cdCommand + blameCommand
   lineNoProb        = []

   blame_output      = subprocess.check_output(['bash','-c', command2Run])
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

rootDir="puppet"
print rootDir
for root, dirs, files in os.walk(rootDir):
    print root
    print dirs
    print files
    print '-'*50
    '''
    for fileName in files:
        print "file name is ",fileName
        file_path_p=os.path.join(rootDir,fileName)
        sloc = sum(1 for line in open(file_path_p))
        count= getDeveloperScatternessOfFile(fileName,rootDir, sloc)



        relDir = os.path.relpath(dir_, rootDir)
        print "relDir is ",relDir
        file_path_p=os.path.join(rootDir,fileName)
        print "file path is ",file_path_p
        sloc = sum(1 for line in open(file_path_p))
        count= getDeveloperScatternessOfFile(relDir, fileName, sloc)
        #relFile = os.path.join(relDir, fileName)        
        print "printing count ",count

#count = getDeveloperScatternessOfFile("C:/Leaky/src/mining/repos/aeroflow/source/factory.js","C:/Leaky/src/mining/repos/aeroflow",100)
#print count
'''