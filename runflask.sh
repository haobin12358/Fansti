DATATIME=$(date +%Y%m%d)
LOGSTART="/tmp/error"
TITLE="/error"
LOGEND=".log"
LOGNAME=$LOGSTART$TITLE$DATATIME$LOGEND
NAME="uwsgi"


echo $"stoping uwsgi...."
if [ ! -n "$NAME" ];then
  echo "no arguments"
  exit;
fi
echo $NAME
ID=`ps -ef | grep uwsgi | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
echo $ID
echo "#####################################"
for id in $ID
do
kill -9 $id
echo "success kill $id"
done
echo "####################################"
echo $"starting run uwsgi....."
echo LOGNAME
if [ ! -d "$LOGSTART" ]; then
 mkdir "$LOGSTART"
fi
if [ ! -f "$LOGNAME" ]; then
 touch "$LOGNAME"
fi
echo BLOGNAME
uwsgi /opt/uwsgiconfig.ini -d ${LOGNAME} -p 8 --threads 10
echo "start ok "

