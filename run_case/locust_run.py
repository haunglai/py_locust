
import os, sys
import queue
from pathlib import Path

root_path=Path(os.path.abspath(__file__)).parent
project=str(Path(root_path).parent)
sys.path.append(project)
sys.path.append(root_path)

from tools.locust_config import run_config,is_run
from tools.commom_function import run_case

case_path=Path(project)/Path(r"locust_case/add_case")


for i in is_run:
    if is_run[i]:
        run_case(case_path/Path(f"{i}.py"),[run_config[i]['user'],run_config[i]['duration']])

