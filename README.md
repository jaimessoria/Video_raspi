# Video_raspi
**Iniciar un nuevo GIT** 
git init 
giit clone *direccion html*
cd *carpeta*
git remote 

**hacer un push**
git add .
git commit -m "agregamos x"
git push

**hacer un pull**
git status
git pull

**Hacer un branch** 

git checkout -b api_telegram
git add -A
git commit -m "api de telegram"
git push -u origin api_telegram

**Para pararte en un branch** 
git checkout api_telegram


**Merge** 
git checkout master
git merge downloader --squash
git commit -m "..."
git push 
