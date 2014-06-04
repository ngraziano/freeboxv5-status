#!/usr/bin/env python
# -*- coding: utf8 -*-

import freebox_v5_status.freeboxstatus
import pprint

# Exit statuses recognized by Nagios and thus by Shinken
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3



fbx = freebox_v5_status.freeboxstatus.FreeboxStatus()
#pprint.pprint( fbx.status )

if fbx.status["adsl"]["ready"]:
    print ('OK - Synchro DOWN %db/s UP %db/s |synchup=%db synchdown=%db attenuationdown=%fdB attenuationup=%fdB margedown=%fdB margeup=%fdB '
        % (fbx.status["adsl"]["synchro_speed"]["down"],fbx.status["adsl"]["synchro_speed"]["up"],fbx.status["adsl"]["synchro_speed"]["up"],fbx.status["adsl"]["synchro_speed"]["down"],fbx.status["adsl"]["attenuation"]["down"],fbx.status["adsl"]["attenuation"]["up"],fbx.status["adsl"]["marge_bruit"]["down"],fbx.status["adsl"]["marge_bruit"]["up"] ))
    raise SystemExit(OK)
else:
    print 'CRITICAL - Not Synchronized'
    raise SystemExit(CRITICAL)


