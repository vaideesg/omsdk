#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Vaideeswaran Ganesan
#
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class iBaseJobApi(object):

    def __init__(self, entity, jobenum):
        self.entity = entity
        self.jobenum = jobenum
        self.reset()

    def reset(self):
        self.last_job = None
        self.jobs_json = {}

    def get_jobs(self):
        return self.entity._get_entries(self.jobs_json, self.jobenum)

    def delete_all_jobs(self):
        pass

    def get_job_details(self, jobid):
        pass

    def get_job_status(self, jobid):
        pass

class iBaseLogApi(object):

    def __init__(self, entity, logenum, logtypesen):
        self.entity = entity
        self.logenum = logenum
        self.logtypesen = logtypesen

    def get_logs(self):
        return self.entity._get_entries(self.jobs_json, self.jobenum)

    def clear_logs(self):
        return self.entity._get_entries(self.jobs_json, self.jobenum)

