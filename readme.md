# setup
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

# db
<!-- ` docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres` -->
https://fastapi.tiangolo.com/tutorial/sql-databases/


# enviroment
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

## docker build

 `docker build --pull --rm -f "Dockerfile" -t rlappdocker:latest "."`

## Run
` docker run -p 8080:8080   rlappdocker:latest `

 then go to `localhost:8080` in a webbrowser

 ## What is running to get imageID
 `docker ps`


## Debugging docker

`docker logs XXXX_imageID`

## docker stop
`docker stop XXXX_imageID`

<!-- docker run -d --name=logtest rlappdocker /bin/sh -c “while true; do sleep 2; df -h; done” -->