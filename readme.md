# Web messenger with microservices
Microservices that work together to make a messaging web application that uses Redis as a datastore.
Messages will automatically expire after a configurable amount of time.

* Storing, retrieving messages (Messages microservice)
* **Nameko** dependency providers (Redis for messages, Postgres for users)
* Sending messages via POST requests
* Displaying messages in the web browser and Browser polling for messages with **JQuery Ajax**
* Securely storing passwords with **Bcrypt** in a Postgres Database
* Authenticating users and Web sessions with **Flask**
* Sign up, Log in, Log out (User microservice)
* Unit testing with **Pytest**

**Requirements**
- [x] Pipenv
- [x] Docker (RabbitMQ, Redis, Postgres)

### Setup
Install dependencies
```shell
pipenv install --dev
```
#### Start a RabbitMQ container
```shell
docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq rabbitmq
```

#### Start a Redis container
```shell
docker run -d -p 6379:6379 --name redis redis
```

#### Start a Postgres container
```shell
docker run --name postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=users -p 5432:5432 -d postgres
```

#### Run the application
*NOTE:* Use different terminals to run the commands (inside project folder)
Run the User microservice:
```shell
nameko run temp_messenger.user_service --config config.yaml
```
Run the Message microservice:
```shell
nameko run temp_messenger.message_service --config config.yaml
```
Run the web server:
```shell
export FLASK_DEBUG=1
export FLASK_APP=temp_messenger/web_server.py
flask run -h 0.0.0.0 -p 8000
```