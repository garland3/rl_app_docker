from datetime import datetime, time
from sqlalchemy.orm import Session
from app.helpers.helpers import row_to_dict
from .schemas import Job, RLConfig
from .database_tables import Alive_t, DesignStatus_t, Job_t,  RLConfig_t


def commit_updates(db: Session):
    """Commit any updates which basically updates the actual db with any changs. """
    db.commit()


def list_2_comma_string(mylist: list):
    """Converts a list to a comman string. """
    return ",".join([str(a) for a in mylist])

# -------------------------------
# --------------- RLConfig ----------
# -------------------------------


def create_RLConfig(db: Session, config: RLConfig, job_id: int):
    """Create an RLConfig object in the database. """
    db_config_obj = RLConfig_t(
        bcs=list_2_comma_string(config.bcs),
        rights=list_2_comma_string(config.rights),
        lefts=list_2_comma_string(config.lefts),
        downs=list_2_comma_string(config.downs),
        ups=list_2_comma_string(config.ups),
        volfraction=config.volfraction,
        uuid=config.uuid,
        job_id=job_id
    )
    db.add(db_config_obj)
    db.commit()
    db.refresh(db_config_obj)
    return db_config_obj


def get_RLConfig(db: Session, job_id):
    """Get an RLConfig object in the database based on job_id"""
    result = db.query(RLConfig_t).filter(RLConfig_t.job_id == job_id).first()
    return result

# -------------------------------
# --------------- Jobs  ----------
# -------------------------------


def create_job(db: Session):
    """Create a job object in the database. """
    myjob = Job_t(timestamp=datetime.now())
    db.add(myjob)
    db.commit()
    db.refresh(myjob)
    return myjob


def get_next_job(db: Session):
    """Get the next job in the queue"""
    result = db.query(Job_t).filter(Job_t.finished == False).first()
    return result


def get_job(db: Session, job_id: int):
    """Get a job object based on the job_id"""
    result = db.query(Job_t).filter(Job_t.id == job_id).first()
    return result


def get_job_being_worked_on(db: Session):
    """Get the job object that is not finished, but is being worked on. """
    result = db.query(Job_t).filter(Job_t.finished == False,
                                    Job_t.working_on_job == True).first()
    return result


def get_most_recent_job(db: Session):
    """Get the most recently created job by time stampl. """
    result = db.query(Job_t).order_by(Job_t.timestamp.desc()).first()
    return result


def set_all_jobs_to_finished(db: Session):
    result = db.query(Job_t).filter(Job_t.finished == False)
    for r in result:
        print(row_to_dict(r))
        r.finished = True
        db.commit()

# -------------------------------
# --------------- DesignStatus_t  ----------
# -------------------------------


def create_DesignStatus(db: Session, job_id: int, progress: int, result: str):
    """Create a new design status object which is the intermediate or final results 
    of the rl algorithm. """
    status = DesignStatus_t(
        job_id=job_id,
        progress=progress,
        timestamp=datetime.now(),
        result=result
    )
    db.add(status)
    db.commit()


def get_most_recent_DesignStatus_with_jobid(db: Session, job_id):
    result = db.query(DesignStatus_t).filter(DesignStatus_t.job_id == job_id).order_by(
        DesignStatus_t.timestamp.desc()).first()
    return result


def get_most_recent_DesignStatus(db: Session):
    result = db.query(DesignStatus_t).order_by(
        DesignStatus_t.timestamp.desc()).first()
    return result


# -------------------------------
# --------------- Alive_t
# Alive object is used to determine if the work is still working/already busy
# or perhaps it failed for some reason and is dead.
# # -------------------------------
def create_Alive(db: Session):
    a = Alive_t(time=datetime.now())
    db.add(a)
    db.commit()
    db.refresh(a)
    print("Created alive record")
    return a


def get_1st_Alive_Time(db: Session):
    result = db.query(Alive_t).first()
    if result == None:
        return None
        # result = create_Alive(db)
    return result.time


def update_Alive_with_now(db: Session):
    result = db.query(Alive_t).first()
    if result == None:
        result = create_Alive(db)
    result.time = datetime.now()
    db.commit()
    return True


def remove_Alive(db: Session):
    result = db.query(Alive_t).first()
    if result == None:
        return
    db.delete(result)
    db.commit()
