from typing import Optional
from fastapi import FastAPI
from fastapi import FastAPI, Request, Response, BackgroundTasks, Depends
# from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from typing import List, Optional
from uuid import uuid1, uuid5
from starlette.middleware.sessions import SessionMiddleware
from app.database.schemas import IntermediateResult, RLConfig, Job, TopResult
from app.database.database import Base, engine, SessionLocal
from app.database import crud
from sqlalchemy.orm import Session
from app.rlconnector.rlconnector import decode_result_from_bytes_to_object, run_rl_code
from app.helpers.helpers import check_if_alive, compute_position_in_queue, encode_json, get_db, row_to_dict

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.add_middleware(SessionMiddleware, secret_key="my_super_secret1290uAAA!!")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if "uuid" not in request.session:
        request.session['uuid'] = str(uuid1())
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit_job_clicked")
async def submit_job_clicked(request: Request, config: RLConfig,
                             background_tasks: BackgroundTasks,
                             db: Session = Depends(get_db)):
    """
    Request a design. Design will be added to the queue. Check if your design is done with 'check_if_done' api
    """
    print(config)
    if "uuid" not in request.session:
        request.session['uuid'] = str(uuid1())
    session = request.session
    config.uuid = session['uuid']
    job = crud.create_job(db)
    crud.create_RLConfig(db, config, job.id)
    background_tasks.add_task(run_rl_code)  # start the worker
    j = row_to_dict(job)
    print(j, type(j))
    return JSONResponse(content=j)


def get_status_return_object(db, job_id):
    status = crud.get_most_recent_DesignStatus_with_jobid(db, job_id)
    result = decode_result_from_bytes_to_object(status.result)
    # status_result = TopResult.parse_raw(status.result)
    # j = {'result':status_result.json()}
    # j = row_to_dict(status)
    return result


@app.post("/check_if_done")
async def check_if_done(request: Request, job: Job,
                        background_tasks: BackgroundTasks,
                        db: Session = Depends(get_db)):
    """
    Check if your design is finished. If finished, returns the json object. If not finished, then returns json {'task':"working"}
    """
    # return {"hi": True}
    # print("Checking if done. ")
    if check_if_alive(db) == False:
        background_tasks.add_task(run_rl_code)
    # cosmos_obj = Cosmos_RLDesign()
    job_t = crud.get_job(db, job.job_id)
    #  -------- IF FINISHED -----------
    if job_t.finished == True:
        # TODO. Add return value.
        if job_t.designstatus:
            j = get_status_return_object(db, job_t.id)
            my_result = IntermediateResult(final_result=True, result=j)
        else:
            my_result = {"job": "fail"}
        print(f"job finished, returning {my_result}")
        return my_result

    # -------- IF the JOB HAS SOME STATUS UPDATES ------
    if len(job_t.designstatus) > 0:
        print("Job's status is greater than 0. Assume working on job. ")
        # TODO. Add return value with real results.
        j = get_status_return_object(db, job_t.id)
        my_result = IntermediateResult(intermediate_results=True, result=j)
        # j.intermediate_results = True
        # print(my_result)
        return my_result

     # -------- ELSE. IT IS IN THE QUEUE. COMPUTE POSITION IN QUEUE ------
    diff = compute_position_in_queue(db, job.job_id)
    return {'task': 'working', 'position': diff}

    # If NOT done, then get the position in the queue
    # if item['done'] == False:
    #     postion = int(cosmos_obj.count_position_in_queue(job.job_id))+1
    #     return {'task': 'working', 'position': postion}
    # # set the item to 'returned to user'
    # cosmos_obj.set_returned_to_user(item)
    # result = item['results']
    # print(f'Returning item to user {result}')
    # return result


@app.get("/clear_queue")
async def clear_queue(secret: str = "None", db: Session = Depends(get_db)):
    """Enable clearing the design queue. Requires knowing the secret key. """
    crud.set_all_jobs_to_finished(db)
    return {"hi": True}
    # if secret != CLEAR_THE_QUEUE_SECRET:
    #     return {"allowed": False}
    # else:
    #     cosmos_obj = Cosmos_RLDesign()
    #     cosmos_obj.clean_up_job_queue()
    #     return {"success": True}
