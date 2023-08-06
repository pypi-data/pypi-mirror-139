#!/usr/bin/env python3
# coding=UTF-8
#
# Copyright 2022. quinn.7@foxmail.com All rights reserved.
# Author :: cat7
# Email  :: quinn.7@foxmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
[ 更新 ]

"""

import re
import subprocess

from rains import __version__


def function_update():
  dos_result = subprocess.Popen(['pip', 'install', 'rains=='], stderr=subprocess.PIPE)
  _out, err = dos_result.communicate()
  newest_version: str = re.findall(r'from versions: (.*)\)', str(err))[0].split(',')[-1].strip()

  message: str
  if newest_version > __version__:
    message = f'发现最新版本: { newest_version }, 正在执行更新程序...'
    print(re.sub('&message&', message, _MESSAGE))
    
    dos_result = subprocess.Popen(['pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = dos_result.communicate()
    if not err:
      print(out)
    else:
      print(err)

  else:
    message = '暂无更新...'
    print(re.sub('&message&', message, _MESSAGE))


_MESSAGE = \
"""
--------------------------------------
 更新
--------------------------------------

 &message&

--------------------------------------
"""
