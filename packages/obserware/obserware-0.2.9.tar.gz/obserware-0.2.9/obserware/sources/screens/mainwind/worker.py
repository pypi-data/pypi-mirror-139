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


import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from obserware.sources.readers.mainwind import (
    tab_network,
    tab_partitions,
    tab_performance,
    tab_processes,
    tab_resources,
)


class Worker(QObject):
    finished = pyqtSignal()
    thrdstat = pyqtSignal(dict)

    @pyqtSlot()
    def threaded_statistics_emitter(self):
        while True:
            time.sleep(1.5)
            statdict = {
                "bottomstat": tab_resources.return_bottombar_threaded_statistics(),
                "perfscreen": tab_performance.return_mainscreen_threaded_statistics(),
                "rsrcscreen": tab_resources.return_mainscreen_threaded_statistics(),
                "procscreen": tab_processes.return_processes_list(),
                "ntwkscreen": {
                    "globrate": tab_network.return_global_network_rate(),
                    "pernicrt": tab_network.return_pernic_threaded_statistics(),
                    "mainscrn": tab_network.return_mainscreen_threaded_statistics(),
                },
                "partscreen": {
                    "counters": tab_partitions.return_storage_counters(),
                    "phptdata": tab_partitions.return_physical_partition_statistics(),
                    "lgptdata": tab_partitions.return_logical_partition_statistics(),
                },
            }
            self.thrdstat.emit(statdict)
