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
from datetime import datetime, timedelta, date
import time

class SchTimer:
    def __init__(self, time_str = None, fmt ="%Y-%m-%d", untilmin=24*60):
        if time_str is None:
            self.time = datetime.now()
        else:
            self.time = datetime.strptime(time_str, fmt)
        self.until = None
        if untilmin is not None:
            self.until = self.time + timedelta(minutes=untilmin)

    def __str__(self):
        mystr = "Time: "+ str(self.time)
        if self.until is not None:
            mystr = mystr + "; Until: "+ str(self.until)
        return mystr

TIME_NOW = SchTimer(time_str = "1970-1-1", untilmin=None)
