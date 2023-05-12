import os, json, sys,requests
import queue
from pathlib import Path
from locust import task,HttpUser
root_path=Path(os.path.abspath(__file__)).parent
project=str(Path(root_path).parent.parent)
print(project)
sys.path.append(project)
sys.path.append(root_path)
from locust_case.base import Base
from tools.commom_function import datatime_numa,run_case,read_csv_to_queue,queue_get_and_put
class case(Base):
    # wait_time = between(0.1,1)
    case_name=(os.path.basename(__file__))[:-3]
    api='/service/space/0.1.0/add'
    parentid=read_csv_to_queue('addbuilding.csv',queue.Queue())
    def body(self):
        return {
            "code":datatime_numa(),
            'parentid':queue_get_and_put(self.parentid),
            'spacename':datatime_numa(),
            'level':datatime_numa()

        }
    @task
    def locust_run(self):

        self.data.put_nowait(self.locust_runcase()['result'][0]['spaceid'])

        # print(person.text)
if __name__=='__main__':
    casename = os.path.basename(__file__)
    run_case(casename,[20,20])

    # print()
    # print(case.body(case))