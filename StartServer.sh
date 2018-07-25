
while read line;do
    echo 'kill ' $line;
    kill $line;
done < runserver.pid
ps -ef | grep runserver | awk '{print $2;}' | xargs kill -9

echo 'Server Will Start 3...'
sleep 1s
echo 'Server Will Start 2...'
sleep 1s
echo 'Server Will Start 1...'
sleep 1s

python3 BackendMock/manage.py runserver 0:12800 &
echo $! > runserver.pid

echo '****** Server Started ******'
