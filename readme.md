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
To add nathan's code. Note: Using the main branch. 
`pip install -e git+https://github.com/nkbrown503/PhDResearch.git@main#egg=rl_top_opt`

# NOTE
* folder `src` is not part of the repo. 