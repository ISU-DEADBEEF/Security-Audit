#!/bin/sh

cecho(){
  LGREEN="\033[1;32m"
  LRED="\033[1;31m"
  YELLOW="\033[1;33m"
  NORMAL="\033[m"
 
  color=\$${1:-NORMAL}
 
  echo -ne "$(eval echo ${color})"
  cat
 
  echo -ne "${NORMAL}"
}

echo "- Creating /usr/local/bin/logger/ directory" | cecho LGREEN
mkdir -p /usr/local/bin/logger/

echo ""
echo "- Copying logger.py to /usr/local/bin/logger/  (init) to /etc/init.d/" | cecho LGREEN
cp logger /etc/init.d/logger
cp logger.py /usr/local/bin/logger/logger.py

echo ""
echo "- CHMODDING files" | cecho LGREEN
chmod +x /etc/init.d/logger /usr/local/bin/logger/logger.py

echo ""
echo "- Done" | cecho LGREEN

echo ""
echo "- Notes:" | cecho YELLOW
echo "- Start service with $ /etc/init.d/logger start" | cecho YELLOW
