from locust import HttpUser,task
import json
import queue
import sys
import os
import logging
from pathlib import Path
# data_path = Path(os.path.abspath(__file__)).parent.parent / Path('data')
# root_path=Path(os.path.abspath(__file__)).parent
# project=str(Path(root_path).parent)
#
# sys.path.append(project)
# sys.path.append(root_path)

from tools.commom_function import wait_run,limit_run_times

class Base(HttpUser):
    data=queue.Queue()
    # case_name=''
    is_log=True
    abstract = True
    data_path = Path(os.path.abspath(__file__)).parent.parent / Path('data')
    if not Path.exists(data_path):
        Path.mkdir(data_path)
    headers = {'Contest-type': 'application/json'}
    def on_stop(self):
        """
        后置步骤：保存写入生成的数据
        :return:
        """
        if self.data.qsize()>0:
            path_csv=self.data_path/Path(f"{self.case_name}.csv")
            data_len=self.data.qsize()
            if Path.exists(path_csv):
                csv="\n"+'\n'.join([self.data.get() for i in range(data_len)])
            else:
                csv='\n'.join([self.data.get() for i in range(data_len)])
            with open(path_csv,'a',encoding='utf-8') as f:
                f.write(csv)


    @wait_run
    def locust_runcase(self):
        body=self.body()
        response = self.client.post(self.api,
                                  headers=self.headers,
                                  data=json.dumps(body)
                                  )

        status_code=response.status_code
        text=response.text
        if status_code!=200 or self.is_log:
            logging.info(f"status_code:{status_code}__body:{body}__response :{text}")
        if status_code!=200:
            print(text)
        return json.loads(response.content.decode('utf-8'))