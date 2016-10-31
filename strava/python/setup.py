#!/usr/bin/python

# Copyright 2016 Guanyu Wang
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

from setuptools import setup

setup(
  name = "strava",
  version = '0.1',
  package_dir = {'stravalib': '.'},
  packages = ['stravalib'],
  description = 'Strava API Python wrapper',
  install_requires=[
          'requests',
  ],
  author = 'Guanyu Wang',
  author_email = 'guanyuwang.cs@gmail.com'
)
