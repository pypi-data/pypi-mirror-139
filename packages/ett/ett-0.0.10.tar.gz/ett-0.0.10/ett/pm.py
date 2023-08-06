import os
import time
import logging

class ExpManager:

    def __init__(self, root:str, 
        project_name:str, exp_name:str='default', 
        work_path:str=os.path.expanduser('~/ett_runs')) -> None:
        self.root = root
        self.pn = project_name
        self.en = exp_name
        self.work_path = work_path
        self.log_path, self.rst_path = self.path_init()

    def path_init(self) -> None:
        # 初始化项目路径
        log_path = os.path.join(self.work_path, self.pn, self.en, 'logs')
        rst_path = os.path.join(self.work_path, self.pn, self.en, 'models')
        os.makedirs(log_path, exist_ok=True)
        os.makedirs(rst_path, exist_ok=True)
        return log_path, rst_path

    def logging_init(self, filename:str=None, format:str=None, 
        datefmt:str=None, level:str="info") -> logging.Logger:
        if filename is None:
            filename = time.strftime("%Y%m%d_%H%M%S", time.localtime())

        if format is None:
            format = "%(asctime)s - %(levelname)s - %(message)s"

        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"
        
        level_dict = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        if level not in level_dict:
            raise ValueError("level must be in {}".format(list(level_dict.keys())))
        else:
            level = level_dict[level]

        filename = os.path.join(self.log_path, filename)
        logging.basicConfig(filename=filename, level=logging.INFO, format=format, datefmt=datefmt)
        return logging.getLogger(filename)