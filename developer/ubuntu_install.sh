sudo apt-get -y install openssl-dev* libsqlite3-dev zlibc zlib1g zlib1g-dev python-pip python-xmlrunner xsever-xephyr
mkdir ~/tmp

echo "Installing Python 2.5"
svn propset svn:ignore -F .svnignore .
pushd ~/tmp
wget -c http://www.python.org/ftp/python/2.5.6/Python-2.5.6.tar.bz2
tar xvfj Python-2.5.6.tar.bz2
pushd Python-2.5.6
./configure >> configure_log.txt
sed 's:LDFLAGS=:LDFLAGS= -L/usr/lib/x86_64-linux-gnu:' <Makefile >Makefile_fix
cp Makefile_fix Makefile
make >> make_log.txt
sudo make altinstall >> make_install_log.txt
popd

echo "Installing Setuptools"
wget -c http://pypi.python.org/packages/2.5/s/setuptools/setuptools-0.6c11-py2.5.egg
sudo sh setuptools-0.6c11-py2.5.egg >> setuptools_install.txt

echo "Installing Django-1.2.7"
wget -c http://www.djangoproject.com/m/releases/1.2/Django-1.2.7.tar.gz
tar xvfz Django-1.2.7.tar.gz
pushd Django-1.2.7
sudo python2.5 setup.py install >> django_install_log.txt 
popd



echo "Installing Pip"
wget -c http://pypi.python.org/packages/source/p/pip/pip-1.0.tar.gz
tar xvfz pip-1.0.tar.gz
pushd pip-1.0
sudo python2.5 setup.py install >> pip_install_log.txt
popd

echo "Installing PyCrypto"
 sudo pip-2.5 install pycrypto==2.0.1

echo "Installing unittest2"
sudo pip-2.5 install unittest2

echo "Installing mock"
sudo pip-2.5 install mock

sudo /usr/bin/pip install selenium
sudo /usr/bin/pip install pyvirtualdisplay

popd

