# EEGImage --Backend
## Quickly Start
1 download or clone this repo to your root (e.g. ~\EEGImage)

2 download python 3.8 and create conda virtual environment

3 install dependencies
```
pip install -r requirement.txt
```
4 add your stability API (https://platform.stability.ai/) to EEGImage\EEGImage\visualizing\draw.py

5 run project
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
