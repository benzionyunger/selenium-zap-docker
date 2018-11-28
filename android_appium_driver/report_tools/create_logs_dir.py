import os
import shutil
from pathlib import Path


class LogsDir:
    current_test_dir = None

    def __init__(self, path_to_main_dir_log=None, dir_name=None):
        self.path_main_logs_dir = path_to_main_dir_log or Path.cwd()
        self.main_logs_dir_name = dir_name or 'logs_dir'

    def create_main_logs_dir(self):
        self.path_main_logs_dir = Path(self.path_main_logs_dir) / self.main_logs_dir_name
        if self.path_main_logs_dir.exists():
            shutil.rmtree(str(self.path_main_logs_dir), ignore_errors=True)

        self.path_main_logs_dir.mkdir()
        os.environ['LOGS_DIR'] = str(self.path_main_logs_dir)
        return str(self.path_main_logs_dir)

    def create_test_log_dir(self, dir_name):
        main_logs_dir = self.path_main_logs_dir or os.environ.get('LOGS_DIR', None)
        test_log_dir = main_logs_dir / dir_name
        test_log_dir.mkdir()
        os.environ['CURRENT_LOGS_DIR'] = str(test_log_dir)
        self.current_test_dir = str(test_log_dir)
