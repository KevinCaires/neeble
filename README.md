# Neeble bot

<img src="https://c.tenor.com/1HAl-cmOzswAAAAd/worms-meninblack.gif">

---

### Dependences

- Python 3.8
- gcc
- python3-dev
- libmysqlclient-dev or similar

Or docker and docker-compose to run into container.

---

### How run

- You need mysql instance running in your pc.
- Into mysql instance create a db named `neeble`.
- Copy file environment/template and rename then.
- Fill environment variables into a new file.
- Load environment varriables with source command
> $ source environment/myenvfile

##### Python local run
- Execute `migrate` command to create necessary tables.
> $ python manage.py migrate
- Excecute `run` command.
> $ python manage.py run

##### Docker run
- Execute the command:
> $ docker-compose up -d --build
