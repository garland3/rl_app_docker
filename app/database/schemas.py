# ----------------------------
# Contains object that are extensions of BaseModel from Fastai
# ----------------------------

from typing import List, Optional
from pydantic import BaseModel
# from datetime import datatime

# class ItemBase(BaseModel):
#     title: str
#     description: Optional[str] = None

# class ItemCreate(ItemBase):
#     pass

# class Item(ItemBase):
#     id: int
#     owner_id: int
#     class Config:
#         orm_mode = True

# class UserBase(BaseModel):
#     email: str

# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True



class RLConfig(BaseModel):
    bcs: List[int]
    rights: List[int]
    lefts: List[int]
    downs: List[int]
    ups: List[int]
    volfraction: float
    uuid: str = ""
    class Config:
      orm_mode = True


class Job(BaseModel):
    job_id: int = 0

class TopResult(BaseModel):
    Topology: List[List[float]]
    SE: List[float]
    VF: List[float]
    class Config:
      orm_mode = True

class IntermediateResult(BaseModel):
    intermediate_results: bool = False
    final_result: bool = False
    result : TopResult

# class DesignStatus(BaseModel):
#     progress : int
#     timestamp : datatime
#     job_id = int
#     result = Column(String, default="")