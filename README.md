# Neeble bot

<img src="https://c.tenor.com/1HAl-cmOzswAAAAd/worms-meninblack.gif" align="center">

---

### Dependencies

- `Python>=3.8`
- `gcc` or your compiler of choice
- `python3-dev`
- Your distro's mysql library (`libmysqlclient-dev` in Ubuntu)

You can also run neeble under [docker](https://www.docker.com/) with [docker-compose](https://docs.docker.com/compose/)

---

### How to run

- Make sure you are running a SQL server instance
- Create a database named `neeble`
- Set up your environment variables with `environment/template` (You may copy the template into a new file)
- Load environment variables with `source`:  
`$ source environment/template`

##### Run it locally using python
The `Makefile` provided will do all necessary migrations and start the bot:  
`$ make production`

##### Run it under python
Build and start the container with `docker-compose`:  
`$ docker-compose up -d --build`
