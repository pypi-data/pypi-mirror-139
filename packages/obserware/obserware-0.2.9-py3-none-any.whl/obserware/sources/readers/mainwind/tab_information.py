"""
Obserware
Copyright (C) 2021-2022 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from datetime import datetime
from os import uname
from sys import version as pythvers

import distro
import psutil
from cpuinfo import CPUINFO_VERSION_STRING as cpuivers
from distro import __version__ as distvers
from psutil import __version__ as psutvers
from PyQt5.QtCore import qVersion as pyqtvers

from obserware import __version__ as obsrvers


def return_software_information():
    retndata = {
        "name": distro.name(),
        "version": distro.version(),
        "hostname": uname().nodename,
        "release": uname().release,
        "rendition": uname().version,
        "boottime": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d, %H:%M:%S"),
    }
    return retndata


def return_obserware_information():
    retndata = {
        "obsrvers": obsrvers,
        "pythvers": pythvers,
        "pyqtvers": pyqtvers(),
        "psutvers": psutvers,
        "cpuivers": cpuivers,
        "distvers": distvers,
    }
    return retndata
