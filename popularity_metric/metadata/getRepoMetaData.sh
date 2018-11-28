#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
  repo_name=$line
  echo "----------------------------------------------------------------------------"
  repo_name=${repo_name%$'\r'}
  echo $repo_name
  jsonFileName=`echo $repo_name | tr '/' _`
  echo $jsonFileName".json"
  #echo "https://api.github.com/repos/"$repo_name
  curl -H "Authorization: token TOKEN_GOES_HERE" -ni "https://api.github.com/repos/"$repo_name -H 'Accept: json' > $jsonFileName.json
  echo "----------------------------------------------------------------------------"
done < "$1" 