from locust import HttpUser,task
import json,queue
import os
import logging
from pathlib import Path
data_path = Path(os.path.abspath(__file__)).parent.parent / Path('data')
class Base(HttpUser):
    data=queue.Queue()
    # case_name=''

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

    def locust_runcase(self):
        body=self.body()
        response = self.client.post(self.api,
                                  headers=self.headers,
                                  data=json.dumps(body)
                                  )
        logging.info(f"body:{body}  response :{response.text}")
        return json.loads(response.content.decode('utf-8'))