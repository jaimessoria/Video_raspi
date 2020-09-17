# Description 

Software in python that capture video, store in NAS and compress to MP4
The hardware used was: Rasberry pi 4 + Camera Module v1

## installation 

**RasPi OS**
1) Install OS: Use the Raspberry Pi Imager for macOS (https://www.raspberrypi.org/downloads/)
2) connect monitor an set the following
3) First, update your system's package list by entering the following command: 
    sudo apt update
    sudo apt full-upgrade
4) Config Raspi to start without monitor hdmi by Adding hdmi_force_hotplug=1 to /boot/config.txt 
    Sudo nano /boot/config.txt
    hdmi_force_hotplug=1
5) Go to Ras pi config and activate SSH and VNC. 
6) Check IP adress with: 
    sudo hostname -I
7) Install vnc viewer in the remote computer and use the IP

**NAS NFS configuration**

sudo mkdir /mnt/nfs
sudo chmod -R 777 /mnt/nfs
sudo chown -R pi:pi /mnt/nfs
sudo mount -t nfs 192.168.0.135:/Users/Leo/Documents/Raspi /mnt/nfs
sudo umount /mnt/nfs

**install GIT**
sudo apt install git
sudo mkdir /git
sudo chmod -R 777 /git
git clone https://github.com/jaimessoria/Video_raspi.git

**install Visual Studio Code**

wget https://packagecloud.io/headmelted/codebuilds/gpgkey -O - | sudo apt-key add -

curl -L https://raw.githubusercontent.com/headmelted/codebuilds/master/docs/installers/apt.sh | sudo bash
**Create Python virtual environment**

Sudo pip3 install virtualenv
virtualenv .env
source .env/bin/activate

**install requirements**  

pip3 install -r /git/Video_raspi/Requirements.txt

**Execute**

python3  /git/Video_raspi/app.py

**Run scrip in startup**
sudo nano /etc/rc.local
sudo python3 /git/Video_raspi/app.py &
sudo reboot
