
#Setting variable for gsutil -- only for google cloud
PATH="$PATH":/snap/bin/gsutil
export BOTO_CONFIG="/home/egarg0587/.boto"
###################

# Deleting the Alert.csv on common cloud storage kept for client
/snap/bin/gsutil rm gs://egarg0587_bucket/Alert.csv

# Removing the filewrite.csv file in case it's there during previous night testing
rm -rf /home/egarg0587/stocktesting/filewrite.csv

# Emptying the Alert.csv and filewriteindex.csv file so that price trigger can run

cat /dev/null > /home/egarg0587/stocktesting/Alert.csv

cat /dev/null > /home/egarg0587/stocktesting/filewriteIndex.csv

# Log in and start writing data to filewrite.csv 

python /home/egarg0587/stocktesting/LoginSamco1.py && sleep 5 && python /home/egarg0587/stocktesting/writeIndex.py &
