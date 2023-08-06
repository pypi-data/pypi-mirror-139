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
[ 版本 ]

"""

import re
import subprocess

from rains import __version__


def function_version():
  dos_result = subprocess.Popen('pip install rains==', stderr=subprocess.PIPE)
  _out, err = dos_result.communicate()
  newest_version: str = re.findall(r'from versions: (.*)\)', str(err))[0].split(',')[-1].strip()
  print(re.sub('&new_version&', newest_version, _MESSAGE))


_MESSAGE = \
f"""
--------------------------------------
 version
--------------------------------------

 本地当前版本: { __version__ }
 线上最新版本: &new_version&

 更新 rains 版本请通过下方命令:

 rains -update

--------------------------------------
"""
