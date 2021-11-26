# Development Setup
Goal is to setup a docker container for development since it is much easier to run a server in Linux than Windows. So, we basically setup a linux dev container. 

* install docker
* install vscode. 
* install vscode remote container dev tools
* install docker extension for vs code. 
* open this folder. 
* select, "reopen in dev container"
* wait for the docker file to build. 
* then in the docker interactive command line terminal, run the following comand. 
```
uvicorn app.main:app --port=8080 --reload
```
* Test by going (in your web browser) to `http://localhost:8080`

# Database
* https://fastapi.tiangolo.com/tutorial/sql-databases/
* https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
*  https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_updating_objects.htm
* I'm using sqlite which is a simple db contained in a file. 
* The db will be a file named `sql_app.db` in the root of the repo when run. 
* I use sqlite studio to open the database and see what is inside. 
    * https://sqlitestudio.pl/
    * Make sure you close it before trying to delete the database file. 
    * If you make changes to the code in python sqlalchamey then it will need to make a new database object. So make sure you close the db and delete the file. This could be avoided with migration strategies, but that is a whole topic by itself. 


# Enviroment
To export the enviroment to the requirements.txt, run
```
pip list --format=freeze > requirements.txt
```
To add nathan's code. Note: Using the main branch. You need to add this to the end of the `requirements.txt`. and comment out the `rl-top-opt` package. 

```
-e git+https://github.com/nkbrown503/PhDResearch.git@main#egg=rl_top_opt
```

# NOTE
* folder `src` is not part of the repo. 

# Docker
This is for setting up the final version. Not the development version. 

1.  docker build
In the root folder of the repo:
 ```
 docker build --pull --rm -f "Dockerfile" -t rlappdocker:latest "."
 ```

2. Run
```
docker run -p 8080:8080   rlappdocker:latest 
```

 then go to `localhost:8080` in a webbrowser

3.  What is running to get imageID
 ```
 docker ps
 ```


4.  Debugging docker

```
docker logs XXXX_imageID
```

5. docker stop
```
docker stop XXXX_imageID
```

6.  Docker push image
```
docker push garland3/rlappdocker:latest
```

7. Pull image
```
docker pull garland3/rlappdocker
```

<!-- docker run -d --name=logtest rlappdocker /bin/sh -c “while true; do sleep 2; df -h; done” -->