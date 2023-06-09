import os, json, sys,requests
import queue
from pathlib import Path
from locust import task,HttpUser
root_path=Path(os.path.abspath(__file__)).parent
project=str(Path(root_path).parent.parent)
sys.path.append(project)
sys.path.append(root_path)
# sys.path.append(r'C:\Users\Administrator\Desktop\py_locust')
from locust_case.base import Base
from tools.commom_function import datatime_numa,run_case,read_csv_to_queue,queue_get_and_put,get_zimu,limit_run_times
class case(Base):
    # wait_time = between(0.1,1)
    case_name=(os.path.basename(__file__))[:-3]
    api='/service/space/0.1.0/add'
    parentid=read_csv_to_queue('addspace.csv',queue.Queue())
    def body(self):
        return {
            "code":get_zimu(),
            'parentid':queue_get_and_put(self.parentid),
            'spacename':"addbuilding_"+get_zimu(),
            'level':get_zimu()

        }
    @task
    def locust_run(self):
        if limit_run_times(self.case_name, self.data):
            self.data.put_nowait(self.locust_runcase()['result'][0]['spaceid'])

        # print(person.text)
if __name__=='__main__':
    casename = os.path.basename(__file__)
    run_case(casename,[20,20])

    # print()
    # print(case.body(case))