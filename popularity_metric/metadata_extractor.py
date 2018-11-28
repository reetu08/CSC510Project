import os 
import csv 
import requests
import json
import pandas as pd 

def getOutputLines(file_name):
    file_lines = []
    with open(file_name, 'rU') as fil:
         file_str = fil.read()
         file_lines = file_str.split('\n')
    return file_lines

def getMetaDataField(field_, str_list):
    val_to_ret = 0
    line = [ s_ for s_ in str_list if field_ in s_]
    if (len(line) > 0 ):
        if ':' in line[0]:
            val_to_ret =  line[0].split(':')[-1].split(',')[0].strip()
            if val_to_ret == 'false':
               val_to_ret = 0 
            if val_to_ret == 'true':
               val_to_ret = 1        
    return str(val_to_ret)

def getCreationDateField(str_list):
    val_to_ret = 0
    line = [ s_ for s_ in str_list if '"created_at":' in s_]
    if (len(line) > 0 ):
        if ':' in line[0]:
            val_to_ret =  line[0].split('"')[3].split('T')[0].strip()
    return str(val_to_ret)
        
def dumpContentIntoFile(strP, fileP):
    print 'called the file writer'
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()

def getMetaData(json_dir_name):
    str_ = ''
    for root_, dirnames, filenames in os.walk(json_dir_name):
        for file_ in filenames:
            if (file_.endswith('json')):
               value = file_.split('.')
               names = value[0].split('_')
               if len(names) > 1: 
                 repo_name = names[0] + '/' + names[1]
                 dir_name = names[1]
                 print 'repo_name ', repo_name
                 print 'dir_name ', dir_name
                 full_p_file = os.path.join(root_, file_)
                 if (os.path.exists(full_p_file)):
                    the_lines=getOutputLines(full_p_file)
                    fork_data    = getMetaDataField('"forks":', the_lines)
                    watcher_data = getMetaDataField('"watchers":', the_lines)
                    stars_data   = getMetaDataField('"stargazers_count":', the_lines)
                    open_issues  = getMetaDataField('"open_issues":', the_lines)
                    start_ts     = getCreationDateField( the_lines)
                    start_data   = start_ts.split('T')[0]
                    the_str      = repo_name + ',' + dir_name + ',' + fork_data + ',' + watcher_data + ',' + stars_data + ',' + open_issues + ',' + start_data  + '\n'
                    print the_str
                    str_ = str_ + the_str
    str_ = 'repo,dir,fork,watcher,star,open_issues,start_date' + '\n'  + str_
    return str_
    
if __name__=='__main__':
    json_dir = 'metadata/'
    out_str = getMetaData(json_dir)
    print out_str
    write_file='metadata_forks_stars_watchers_starttime_output.csv'
    dumpContentIntoFile(out_str, write_file)