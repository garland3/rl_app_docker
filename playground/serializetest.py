import numpy as np
from pydantic.main import BaseModel
from typing import List, Optional

n = 5
Mat_Plot = np.zeros(shape  = (n**2,))
Max_SE_Ep = 1.0
VoidCheck= 0.5


App_Plot={}
App_Plot['Topology']=[]
App_Plot['SE']=[]
App_Plot['VF']=[]
App_Plot['Topology'].append([str(x) for x in Mat_Plot])
App_Plot['SE'].append(str(round(Max_SE_Ep,1)))
App_Plot['VF'].append(str(round(VoidCheck)))

# print(App_Plot)



class TopResult(BaseModel):
    Topology: List[List[float]]
    SE: List[float]
    VF: List[float]
    class Config:
        orm_mode = True

class IntermediateResult(BaseModel):
    intermediate_results: bool = True
    result : TopResult


result2 = TopResult.parse_obj(App_Plot)

# print(result2)
s = result2.json()
b = bytearray()
b.extend(map(ord, s))
print(b)
print("--"*20)
print(s)

print("--"*20)
decoded_s = b.decode("utf-8") 
j = TopResult.parse_raw(decoded_s)
# att
# j = get_status_return_object(db, job_t.id)
my_result = IntermediateResult(intermediate_results = True, result = j)
# j.intermediate_results = True
print(my_result)