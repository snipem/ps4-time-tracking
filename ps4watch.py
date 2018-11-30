#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import pyps4
import datetime

playstation = pyps4.Ps4("0.0.0.0", broadcast=True)

dateTime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M+0000")

appName = None
titleId = None

try:
    appName = playstation.get_running_app_name()
    titleId = playstation.get_running_app_titleid()
except KeyError as err:
    # Expected error if PS4 is not online
    pass

print("%s,%s,%s" %
      (dateTime,
       (appName if appName else "null"),
       (titleId if titleId else "null")))
