# Photographers app 

> This is application for customers who search photographers 
> and for photographers who search customers
> 
> 


Запуск:

    docker-compose build && docker-compose up -d
    docker exec -it app alembic -c /code/app/alembic.ini upgrade head