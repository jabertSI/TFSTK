#Mettre le proxy
git config --global https.proxy http://10.100.100.242:80
git config --global http.proxy http://10.100.100.242:80
#Enlever le proxy
git config --global unset http.proxy 
git config --global unset https.proxy