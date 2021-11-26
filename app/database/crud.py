from datetime import datetime, time
from sqlalchemy.orm import Session

from app.helpers.helpers import row_to_dict

from .schemas import Job, RLConfig
from .database_tables import Alive_t, DesignStatus_t, Job_t,  RLConfig_t

# def create_user(db: Session, user: UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_updating_objects.htm


def commit_updates(db: Session):
    db.commit()


def list_2_comma_string(mylist: list):
    return ",".join([str(a) for a in mylist])

# def string_with_commas_to_list(string):


def create_job(db: Session):
    myjob = Job_t(timestamp=datetime.now())
    db.add(myjob)
    db.commit()
    db.refresh(myjob)
    return myjob


def create_RLConfig(db: Session, config: RLConfig, job_id: int):
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
    result = db.query(RLConfig_t).filter(RLConfig_t.job_id == job_id).first()
    return result


def get_next_job(db: Session):
    result = db.query(Job_t).filter(Job_t.finished == False).first()
    return result


def get_job(db: Session, job_id: int):
    result = db.query(Job_t).filter(Job_t.id == job_id).first()
    return result


def get_job_being_worked_on(db: Session):
    result = db.query(Job_t).filter(Job_t.finished == False,
                                    Job_t.working_on_job == True).first()
    return result


def get_most_recent_job(db: Session):
    result = db.query(Job_t).order_by(Job_t.timestamp.desc()).first()
    return result
# def get_job(db:Session, uuid:int ):
#     result = db.query(Job_t).filter(Job_t.id == job_id).first()
#     return result

    # db.refresh


def create_DesignStatus(db: Session, job_id: int, progress: int, result: str):
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
    # filter(Job_t.finished == False).first()


def set_all_jobs_to_finished(db: Session):
    result = db.query(Job_t).filter(Job_t.finished == False)
    for r in result:
        print(row_to_dict(r))
        r.finished = True
        db.commit()
    # db.refresh()


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
