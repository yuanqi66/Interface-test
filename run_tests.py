# @Time: 2021/9/16 0:16
# @File: run_tests.py
# @Author: YuanQi
# @Email: 1252429141@qq.com

import time, sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader
from db_fixture import test_data


# 指定测试用例为当前文件夹下的interface目录
test_dir = './interface'
# 查找interface目录下所有以“_test.py"结尾的测试文件
testsuit = defaultTestLoader.discover(test_dir, pattern='*_test.py')

if __name__ == "__main__":
    test_data.init_data()       # 初始化接口测试数据

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='Guest Manage System Interface Test Report',
                            description='Implementation Example with:')
    runner.run(testsuit, rerun=0, save_last_run=False)
    fp.close()
