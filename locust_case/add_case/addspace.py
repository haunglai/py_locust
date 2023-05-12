import os, json, sys,requests
from pathlib import Path
from locust import task,HttpUser,between
root_path=Path(os.path.abspath(__file__)).parent
project=str(Path(root_path).parent.parent)
print(project)
sys.path.append(project)
sys.path.append(root_path)
from locust_case.base import Base
from tools.commom_function import get_zimu,run_case
class case(Base):
    # wait_time = between(1,3)
    case_name=(os.path.basename(__file__))[:-3]
    api='/service/space/0.1.0/add'
    def body(self):
        return {
            "code":get_zimu(),
            'parentid':get_zimu(),
            'spacename':'space_'+get_zimu(),
            'level':get_zimu()

        }
    @task
    def locust_run(self):
        self.data.put_nowait(self.locust_runcase()['result'][0]['spaceid'])

        # print(person.text)
if __name__=='__main__':
    casename = os.path.basename(__file__)
    run_case(casename,[10,100])

    # print()
    # print(case.body(case))