import os,subprocess,json,random,requests,urllib3,datetime

from locust import HttpUser,task,between
class asss(HttpUser):
    wait_time = between(0.1,1)
    @task
    def device(self):
        device=self.client.post('/adddevice',
                           headers={'contest-type':'application/json'},
        data=json.dumps({'person':''.join([chr(random.randint(97,111)) for i in range(20)])}))
if __name__=='__main__':
    casename=os.path.basename(__file__)
    aa=datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    cmd=f'locust -f {casename} -r 10 -t 50 --host=http://127.0.0.1:8000 --headless --html={casename[:-3]}{aa}.html'
    a=subprocess.Popen(cmd)
    a.wait()
