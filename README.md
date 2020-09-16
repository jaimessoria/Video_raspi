# Run Application

Software in python that capture video, store in NAS and compress to MP4
The hardware used was: Rasberry pi 4 + Camera Module v1

**Create Python virtual environment**

pyenv global 3.7.4
Sudo pip3 install virtualenv
virtualenv .env
source .env/bin/activate

**install requirements**  

pip3 install -r Requirements.txt

**Execute**

python3  app.py