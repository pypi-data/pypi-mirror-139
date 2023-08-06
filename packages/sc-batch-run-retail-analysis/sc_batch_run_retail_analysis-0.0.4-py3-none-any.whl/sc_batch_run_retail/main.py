# The MIT License (MIT)
#
# Copyright (c) 2022 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import logging
import os
import os.path
from datetime import datetime

from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

from sc_batch_run_retail import PROJECT_NAME, __version__
from sc_retail_analysis.main import main as retail_main
from sc_diff_analysis.main import main as diff_main
from sc_config import ConfigUtils


class Runner(metaclass=Singleton):

    def __init__(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)
        self._rerun_dates: list = list()

    def process_directory(self, date_str, fullpath):
        conf_file = os.path.join(fullpath, "production.yml")
        if not (os.path.exists(conf_file) and os.path.isfile(conf_file)):
            logging.getLogger(__name__).info(f"未找到配置文件，忽略此日期: {date_str}")
            return 0
        logging.getLogger(__name__).info(f"处理文件夹：{date_str}")
        os.chdir(fullpath)
        # 跑零售的时点分析
        result = retail_main()
        return result

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).debug("configurations {}".format(self._config.as_dict()))
        config = self._config
        # 零售批量重跑日期列表
        rerun_dates = config.get("batch.retail_rerun_dates")
        if rerun_dates is not None and type(rerun_dates) is list:
            for item in rerun_dates:
                self._rerun_dates.append(str(item))

        path = os.getcwd()
        date_dirs = dict()
        # 扫描日期文件夹
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.startswith('.') or entry.is_file():
                    continue
                try:
                    datetime.strptime(entry.name, "%Y%m%d")
                except ValueError:
                    # 不是日期文件夹，则忽略
                    continue
                if entry.name not in self._rerun_dates:
                    # 不在此次需要重跑的日期列表中，则忽略
                    continue
                date_dirs[entry.name] = entry.path
        # 将文件夹按日期前后顺序排序
        date_dirs = dict(sorted(date_dirs.items()))
        logging.getLogger(__name__).info(f"待处理日期列表：{date_dirs.keys()}")
        for date_str, full_path in date_dirs.items():
            result = self.process_directory(date_str=date_str, fullpath=full_path)
            if result != 0:
                return result
        # 跑零售的差异分析
        conf_file = os.path.join(path, "production.yml")
        if os.path.exists(conf_file) and os.path.isfile(conf_file):
            os.chdir(path)
            result = diff_main()
            return result
        return 0


def main():
    try:
        parser = argparse.ArgumentParser(description='batch run retail analysis')
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
