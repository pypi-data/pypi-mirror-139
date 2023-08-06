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


import psutil
from cpuinfo import get_cpu_info

from obserware.sources.readers import frequency, time

freqvalu = frequency()
timevalu = time()


def return_mainscreen_threaded_statistics():
    retndata = {}
    cputsecs, cputperc, cputqant = (
        psutil.cpu_times(percpu=True),
        psutil.cpu_times_percent(percpu=True),
        psutil.cpu_count(),
    )
    cpudfreq, cpudperc = (psutil.cpu_freq(percpu=True), psutil.cpu_percent(percpu=True))
    for indx in range(cputqant):
        retndata[indx] = {
            "cpuclock": {
                "usejperc": int(cpudperc[indx]),
                "cpudhrtz": {
                    "cpumaxhz": freqvalu.format(cpudfreq[indx].max),
                    "cpuminhz": freqvalu.format(cpudfreq[indx].min),
                    "cpucurhz": freqvalu.format(cpudfreq[indx].current),
                },
            },
            "cputimes": {
                "time": {
                    "cputusnm": timevalu.format(cputsecs[indx].user),
                    "cputuspr": timevalu.format(cputsecs[indx].nice),
                    "cputkrnm": timevalu.format(cputsecs[indx].system),
                    "cputnull": timevalu.format(cputsecs[indx].idle),
                    "cputiowt": timevalu.format(cputsecs[indx].iowait),
                    "cputhirq": timevalu.format(cputsecs[indx].irq),
                    "cputsirq": timevalu.format(cputsecs[indx].softirq),
                    "cputvirt": timevalu.format(cputsecs[indx].steal),
                    "cputgest": timevalu.format(cputsecs[indx].guest),
                    "cputgtnc": timevalu.format(cputsecs[indx].guest_nice),
                },
                "perc": {
                    "cputusnm": cputperc[indx].user,
                    "cputuspr": cputperc[indx].nice,
                    "cputkrnm": cputperc[indx].system,
                    "cputnull": cputperc[indx].idle,
                    "cputiowt": cputperc[indx].iowait,
                    "cputhirq": cputperc[indx].irq,
                    "cputsirq": cputperc[indx].softirq,
                    "cputvirt": cputperc[indx].steal,
                    "cputgest": cputperc[indx].guest,
                    "cputgtnc": cputperc[indx].guest_nice,
                },
            },
        }
    return retndata


def return_cpu_specifications_information():
    retndata = {
        "name": get_cpu_info().get("brand_raw"),
        "vendor": get_cpu_info().get("vendor_id_raw"),
        "frequency": get_cpu_info().get("hz_advertised_friendly"),
        "count": get_cpu_info().get("count"),
        "bits": get_cpu_info().get("bits"),
        "arch": get_cpu_info().get("arch"),
        "stepping": get_cpu_info().get("stepping"),
        "model": get_cpu_info().get("model"),
        "family": get_cpu_info().get("family"),
    }
    return retndata


def return_feature_flags_information():
    retndata = {"featflag": []}
    if get_cpu_info().get("flags"):
        retndata["featflag"] = get_cpu_info().get("flags")
    return retndata
