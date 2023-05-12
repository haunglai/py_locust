import random
import subprocess,datetime,os,queue
from pathlib import Path
import sys

root_path=Path(os.path.abspath(__file__)).parent
project=root_path.parent

sys.path.append(str(root_path))
sys.path.append(str(project))
from pathlib import Path
from tools.setting import host
dir_path=datetime.datetime.now().strftime("%Y%m%d")
case_path=Path(os.path.abspath(__file__)).parent.parent.parent/Path(dir_path)
if not Path.exists(case_path):
    Path.mkdir(case_path)
def run_case(casename,runtime):
    """

    拉起locust运行用例
    :param casename:
    :param runtime:
    :return:
    """
    report=f"""{(os.path.split(casename)[-1])[:-3]}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}"""
    report_path=case_path/Path(report)
    if not Path.exists(report_path):
        Path.mkdir(report_path)
    cmd = f'locust -f {casename} -r {runtime[0]} -u {runtime[0]} -t {runtime[1]} --host={host} --headless --csv={report_path}\\{report}  ' \
          f' --html={report_path}\\{report}.html --logfile={report_path}\\{report}.log'
    a = subprocess.Popen(cmd)
    a.wait()

a=queue.Queue()

def datatime_numa():
    """
    利用时间的唯 一性，生成唯一的数字字符串


    :return:
    """
    if a.qsize()<5:
        for i in range(11,99):
            a.put_nowait(i)
    b=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    return b+str(a.get())
def num_to_list(num,num_list):
    """
    类似于十进制转为十进制
    :param num:
    :param num_list:
    :return:
    """
    return num_list if num//13<1 else num_to_list(num//13,num_list+[num%13])
def get_zimu():
    """

    :return:
    """
    a=num_to_list(int(datatime_numa()),[])
    c=[chr(int(i)+random.choice([97,110,65,78])) for i in a]
    return ''.join(c)



def read_csv_to_queue(csv,a:queue.Queue):
    """
    读取csv文件放出队列里

    :param csv:
    :param a:
    :return:
    """
    csv_path=Path(os.path.abspath(__file__)).parent.parent/Path(f"data/{csv}")
    with open(csv_path,'r',encoding='utf-8')as f:
        csv_list=f.read().split('\n')
    for i in csv_list:
        if i:
            a.put_nowait(i)
    return a
def queue_get_and_put(a:queue.Queue):
    """
    将队列拿出来，将放进来

    :param a:
    :return:
    """
    b=a.get()
    a.put_nowait(b)
    return b

if __name__=="__main__":
    print(get_zimu())