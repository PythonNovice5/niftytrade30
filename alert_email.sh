#!/bin/bash

# This script will place order and send email if a trade is there

#Setting variable for gsutil -- only for google cloud
PATH="$PATH":/snap/bin/gsutil
export BOTO_CONFIG="/home/egarg0587/.boto"
###################


today=`date +%Y-%m-%d.%H:%M:%S`
subject=`cat /home/egarg0587/stocktesting/Alert.csv`

if [[ $(echo $subject) ]]; then
        echo "Found content in file, so doing nothing."
else
	# Checking if a trade is there to be taken
        python /home/egarg0587/stocktesting/OHLC.py
        subject=`cat /home/egarg0587/stocktesting/Alert.csv`
        if [[ $(echo $subject) ]]; then

		#Placing file for client over shared storage
		/snap/bin/gsutil cp /home/egarg0587/stocktesting/Alert.csv gs://egarg0587_bucket/Alert.csv 2> /dev/null &
		#################################################

		# Trade found so placing order and sending email
		python /home/egarg0587/stocktesting/PlaceOrder.py > /home/egarg0587/stocktesting/logs/PlaceOrder.log.$today 2>&1
                echo "Check the subject" | mail -s $subject akthesedays@gmail.com garg.eshant@gmail.com
                echo "Mail sent"
        else
                echo "No trade to execute"
        fi
fi
