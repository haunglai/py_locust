import os, sys
from pathlib import Path

root_path=Path(os.path.abspath(__file__)).parent
project=str(Path(root_path).parent)
sys.path.append(project)
sys.path.append(root_path)
from tools.log import logger

csv_path=Path(project)/Path('data')
csv_list=os.listdir(csv_path)
for i in csv_list:
    csv=Path(csv_path)/Path(i)
    os.r(csv)
    logger.info(f"已删除文件：{csv}")