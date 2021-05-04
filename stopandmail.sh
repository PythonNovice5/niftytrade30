
#!/bin/bash
. /home/egarg0587/.bashrc

#kill process

pid=`ps -ef | grep writeIndex.py | grep -v grep | awk '{print $2}'`
kill -9 $pid

# Email the file

echo "Data for today" | mail -s "Today's data" -A "/home/egarg0587/stocktesting/filewrite.csv" akthesedays@gmail.com garg.eshant@gmail.com

# Moving file to archive

today=`date +%Y-%m-%d.%H:%M:%S`
mv /home/egarg0587/stocktesting/filewrite.csv /home/egarg0587/stocktesting/archive/filewrite_$today.csv


