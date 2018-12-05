import os
import subprocess
import sys
from pathlib import Path


class LogcatFile:
    logcat_process = None
    file_path = None

    def __init__(self, file_path=None, filter_by=None):
        if file_path:
            self.file_path = Path(file_path)
        else:
            self.file_path = os.environ.get("CURRENT_LOGS_DIR", None)

        self.file_path = self.file_path / 'logcat.log'
        self.filter_by = filter_by

    def open_logcat_file(self, file_path=None):
        if file_path:
            file_path = Path(file_path) / 'logcat.log'
        else:
            file_path = self.file_path
        pl = sys.platform

        if 'win' in pl:

            with open(str(file_path), 'w') as logfile:
                subprocess.call('adb logcat -c'.split())
                if self.filter_by:
                    self.logcat_process = subprocess.Popen('adb logcat | findstr {}'.format(self.filter_by).split(),
                                                           stdout=logfile)
                else:
                    self.logcat_process = subprocess.Popen('adb logcat'.split(), shell=True, stdout=logfile)
        else:
            with open(str(file_path), 'w') as logfile:
                subprocess.call('/opt/android-sdk-linux/platform-tools/adb logcat -c'.split())
                if self.filter_by:
                    self.logcat_process = subprocess.Popen(
                        "/opt/android-sdk-linux/platform-tools/adb -s emulator-5554 logcat | grep {}".
                            format(self.filter_by).split(" "), stdout=logfile)

    def stop_logcat(self):
        self.logcat_process.kill()
