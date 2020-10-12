Besides the installation of the dependencies listed in requirements.txt a docker container is required to use django channels with layers.
For the battleship application the basic command from django-channels tutorial can be used.

```docker run -p 6379:6379 -d redis:5```

The django backend should be started with port 8080. It can be started in the 'django-be/battleship' folder with following command:

```python manage.py runserver 8080```

The vue frontend will then automatically use port 8081. It can be started in 'vue-fe/battleship' with:

```npm run serve```
