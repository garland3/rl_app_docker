import functools
from multiprocessing import Process
import traceback
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.database import crud
from app.helpers.helpers import (
    ALIVE_FILENAME, DEBUGGING, MAX_DEAD_TIME, MAX_JOB_RUN_TIME_SECONDS,
    check_if_alive, get_db, row_to_dict,
    say_im_alive, say_im_dead)
from app.database.database_tables import RLConfig_t
from app.database.schemas import TopResult


def encode_result_to_bytes(result):
    result2 = TopResult.parse_obj(result)
    # print(result2)
    s = result2.json()
    b = bytearray()
    b.extend(map(ord, s))
    return b


def decode_result_from_bytes_to_object(b):
    decoded_s = b.decode("utf-8")
    result2 = TopResult.parse_raw(decoded_s)
    return result2


def save_results_design_in_DB(db: Session, job_id,  result):
    """Save the intermediate OR Final results in the DB
    """
    print(f"save_results_design_in_DB is called. {job_id}")
    say_im_alive(db)
    # result_as_string = json.dumps(result)
    b = encode_result_to_bytes(result)
    crud.create_DesignStatus(db, job_id, progress=1, result=b)


def clean_config_obj(config: RLConfig_t):
    """Basically convert strings seperated by commans to lists

    if it is an empty list, then set as []"""
    config = row_to_dict(config)
    for n in ['bcs', 'rights', 'lefts', 'downs', 'ups']:
        if config[n] == "":
            config[n] = []
            continue
        config[n] = config[n].split(",")
    return config


def run_rl_job(job_id):
    """Run Nathan's RL code for one job. """
    db = next(get_db())
    job = crud.get_job(db, job_id=job_id)
    job.working_on_job = True
    crud.commit_updates(db)
    print(f"run_rl_job {job_id}")
    config = crud.get_RLConfig(db, job_id)
    config = clean_config_obj(config)
    print(f"Run RL code with config {config}")

    try:
        # ------------------------------------------
        # ------------ NATHAN'S CODE ----CALLED HERE
        # ------------------------------------------
        from Top_Opt_RL.DQN import main as r
        from Top_Opt_RL.DQN.opts import parse_opts
        # cosmos_obj = Cosmos_RLDesign()
        opts = parse_opts([""])
        envs = r.EnviromentsRL(opts)

        # if DEBUGGING == True:
        #     print("quick return while debugging")
        #     return
        db_save_fn = functools.partial(save_results_design_in_DB, db, job.id)
        result = r.TopOpt_Designing(config, opts, envs, [db_save_fn])

        # ------------------------------------------
        # ------------ END NATHAN'S CODE ----
        # ------------------------------------------
        save_results_design_in_DB(db, job.id, result=result)
    except Exception as e:
        print("-"*30)
        print(f"Failed to run RL code with error {e}")
        print(traceback.format_exc())
        traceback.print_stack()
        print("-"*30)
    finally:
        print(f"Calling finish on rl job {job.id}")
        job.finished = True
        crud.commit_updates(db)


def run_rl_code():
    """
    Runs the background work of actually making the design
    """
    db = next(get_db())
    if check_if_alive(db) == False:
        try:
            say_im_alive(db)
            # keep getting new jobs. Limit to 100 jobs in the queue.
            for i in range(3):
                try:
                    job = crud.get_next_job(db)
                    if job is None:
                        print("No more jobs ")
                        return  # if we are finished, then exit.
                    print(f"Starting worker for job_id: {job.id}")
                    p1 = Process(target=run_rl_job, args=(job.id,))
                    p1.start()
                    p1.join(timeout=MAX_JOB_RUN_TIME_SECONDS)
                    if p1.exitcode == None:
                        print("Designing timed out. ")
                        job.finished = True
                        job.message = "Timed out. Design took too long. "
                        crud.commit_updates(db)
                        # cosmos_obj.update_job_with_failure(job)
                except Exception as jobFail:
                    print(f"Designing Job Failed {jobFail}")
                    job.finished = True
                    job.message = "Some error occured while processing the design."
                    crud.commit_updates(db)
        except Exception as e:
            print(f"Caught some error. :( . Messaage = {e}")
        finally:
            say_im_dead(db)
            print("RL worker stopping. ")
    else:
        print("Job queue is already running. Ending this worker ")
