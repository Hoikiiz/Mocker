
while read line;do
    echo 'kill ' $line;
    kill $line;
done < runserver.pid
ps -ef | grep runserver | awk '{print $2;}' | xargs kill -9

sleep 1s
echo '****** Server Stoped ******'
