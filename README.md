<h1> Avito </h1>
JSON API сервис сделан на фреймворке Django и Django-REST-Framework. Используемая СУБД PostgreSQL.

### Команды для запуска Docker:

```
git clone https://github.com/prostomusa/Avito.git
cd Avito
docker-compose build
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up
```

### Ссылка на документацию API:
[https://documenter.getpostman.com/view/7641548/TVmMgdL1]
