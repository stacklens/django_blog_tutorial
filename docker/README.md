# django-blog with docker

## quict start

run with docker

```shell
docker run -d --restart=always --name=blog \
  -p 8088:80 \
  willdockerhub/django-blog
```

create superuer

```shell
docker exec -it blog python manage.py createsuperuser --username admin
```


accee browers
```
http://192.168.1.1:8088
```
