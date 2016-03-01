# GalileoPyServer
The goal of every IoT device is to blink an LED. This is an example of doing that in flask. A sample web server using Flask that can read digital &amp; analog sensors as well as control an LED. 


To use this you must install flask. The easiest way is using pip. If you don't have pip follow these instructions. 

Pip relies on ez_setup, so install that first. If you have not installed PIP, follow these instructions.

    curl https://bootstrap.pypa.io/ez_setup.py -o ez_seetup.py
    python ez_setup.py --insecure
    
Then you must install PIP.

    curl  https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz -o pip-8.0.2.tar.gz
    tar -zxvf pip-8.0.2.tar.gz
    cd pip-8.0.2
    python setup.py build install

Then install Flask

    pip install Flask 

This app uses https to prevent passing credentials in the clear. As such you need to install pyopenssl.

    pip install pyopenssl

The app requires a username of admin and password of galileo to control the LED. The password is a sha512, which is stored in server.sql3. 

A sample server.crt and server.key is here for download. You should probably create your own. 

Pic of Web Interface
![alt tag](https://raw.githubusercontent.com/joemcmanus/GalileoPyServer/master/pyserver.png)

Sample Wiring 
![alt_tag](https://raw.githubusercontent.com/joemcmanus/GalileoPyServer/master/GalileoGen2-PyServer_bb.png)
