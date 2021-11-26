# ----------------------------
# Contains object that are extensions of BaseModel from Fastai
# ----------------------------

from typing import List, Optional
from pydantic import BaseModel


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
    result: TopResult
