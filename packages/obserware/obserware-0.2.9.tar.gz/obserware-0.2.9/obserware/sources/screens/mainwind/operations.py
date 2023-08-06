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


import logging
import sys
import time
from datetime import datetime

from PyQt5.QtChart import QChart, QPieSeries
from PyQt5.QtCore import QSize, QThread
from PyQt5.QtGui import QCloseEvent, QColor, QFont, QPainter
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDesktopWidget,
    QHeaderView,
    QListWidgetItem,
    QMainWindow,
    QTableWidgetItem,
)

from obserware import __version__
from obserware.sources.readers.mainwind import (
    tab_information,
    tab_network,
    tab_partitions,
    tab_performance,
    tab_resources,
)
from obserware.sources.readers.procwind.provider import check_process_existence
from obserware.sources.screens.mainwind.interface import Ui_mainwind
from obserware.sources.screens.mainwind.worker import Worker
from obserware.sources.screens.procwind.operations import ProcWind
from obserware.sources.widgets.lgptwdgt.operations import LgPtWdgt
from obserware.sources.widgets.ntwkwdgt.operations import NtwkWdgt
from obserware.sources.widgets.perfwdgt.operations import PerfWdgt
from obserware.sources.widgets.phptwdgt.operations import PhPtWdgt

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(message)s",
    datefmt="[%H:%M:%S] [%d %b %Y]",
)


class MainWind(QMainWindow, Ui_mainwind):
    def __init__(self):
        QMainWindow.__init__(self)
        self.title = "Obserware v%s" % __version__
        self.setupUi(self)
        self.setWindowTitle(self.title)
        self.obj = Worker()
        self.thread = QThread()
        self.cpud_time_series = QPieSeries()
        self.cpud_donut_chart = QChart()
        self.memo_time_series = QPieSeries()
        self.memo_donut_chart = QChart()
        self.swap_time_series = QPieSeries()
        self.swap_donut_chart = QChart()
        self.perfwgls, self.ntwkwgls, self.phptwgls, self.lgptwgls = [], [], [], []
        self.statusBar.setFont(QFont("Inter", 10))
        self.statusBar.setStyleSheet("background-color: rgba(128, 128, 128, 0.5);")
        self.statusBar.setSizeGripEnabled(False)
        self.initialize_window_on_screen_center()
        self.initialize_elements()
        self.obj.thrdstat.connect(self.refresh_elements)
        self.obj.moveToThread(self.thread)
        self.thread.started.connect(self.obj.threaded_statistics_emitter)
        self.thread.start()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.thread.destroyed.connect(sys.exit())

    def initialize_window_on_screen_center(self):
        rectfrme = self.frameGeometry()
        cntrloca = QDesktopWidget().availableGeometry().center()
        rectfrme.moveCenter(cntrloca)
        self.move(rectfrme.topLeft())

    def open_process_window(self, rowe, colm):
        try:
            prociden = self.proctree.item(rowe, 0).text()
            if check_process_existence(int(prociden)):
                self.procwdis = ProcWind(prociden, self.statusBar, parent=self)
                self.procwdis.exec()
            else:
                logging.warning("PID %s could not be retrieved as it does not exist" % prociden)
                self.statusBar.showMessage(
                    "[%s] PID %s could not be retrieved as it does not exist"
                    % (datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"), prociden)
                )
        except AttributeError:
            pass

    def initialize_bottombar_statistics(self):
        retndata = tab_resources.return_bottombar_onetimed_statistics()
        self.userhost.setText("%s@%s" % (retndata["username"], retndata["hostname"]))
        self.kernvers.setText("%s %s" % (retndata["systname"], retndata["rlsename"]))

    def refresh_bottombar_statistics(self, statdict):
        self.cpudperc.setText(str(statdict["bottomstat"]["cpud_percent"]))
        self.memoperc.setText(str(statdict["bottomstat"]["memo_percent"]))
        self.swapperc.setText(str(statdict["bottomstat"]["swap_percent"]))
        self.diskperc.setText(str(statdict["bottomstat"]["disk_percent"]))

    def initialize_resources_tabscreen(self):
        self.cpud_time_series.setHoleSize(0.60)
        self.cpud_donut_chart.setBackgroundBrush(QColor("transparent"))
        self.cpud_time_series.append("Free", 0.0)
        self.cpud_time_series.append("Used", 0.0)
        self.cpud_donut_chart.legend().hide()
        self.cpud_donut_chart.addSeries(self.cpud_time_series)
        self.cpud_donut_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.cpud_donut_chart.setContentsMargins(-50, -50, -50, -50)
        self.cpudgfvw.setChart(self.cpud_donut_chart)
        self.cpudgfvw.setRenderHint(QPainter.Antialiasing)
        self.memo_time_series.setHoleSize(0.60)
        self.memo_donut_chart.setBackgroundBrush(QColor("transparent"))
        self.memo_time_series.append("Free", 0.0)
        self.memo_time_series.append("Cached", 0.0)
        self.memo_time_series.append("Used", 0.0)
        self.memo_time_series.append("Free", 0.0)
        self.memo_time_series.append("Used", 0.0)
        self.memo_donut_chart.legend().hide()
        self.memo_donut_chart.addSeries(self.memo_time_series)
        self.memo_donut_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.memo_donut_chart.setContentsMargins(-50, -50, -50, -50)
        self.memogfvw.setChart(self.memo_donut_chart)
        self.memogfvw.setRenderHint(QPainter.Antialiasing)
        self.swap_time_series.setHoleSize(0.60)
        self.swap_donut_chart.setBackgroundBrush(QColor("transparent"))
        self.swap_time_series.append("Free", 0.0)
        self.swap_time_series.append("Used", 0.0)
        self.swap_time_series.append("Free", 0.0)
        self.swap_time_series.append("Used", 0.0)
        self.swap_donut_chart.legend().hide()
        self.swap_donut_chart.addSeries(self.swap_time_series)
        self.swap_donut_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.swap_donut_chart.setContentsMargins(-50, -50, -50, -50)
        self.swapgfvw.setChart(self.swap_donut_chart)
        self.swapgfvw.setRenderHint(QPainter.Antialiasing)

    def refresh_resources_tabscreen(self, statdict):
        self.cpud_time_series.slices()[0].setValue(100 - statdict["bottomstat"]["cpud_percent"])
        self.cpud_time_series.slices()[1].setValue(statdict["bottomstat"]["cpud_percent"])
        self.memo_time_series.slices()[0].setValue(
            statdict["rsrcscreen"]["memo"]["percentage"]["free"]
        )
        self.memo_time_series.slices()[1].setValue(
            statdict["rsrcscreen"]["memo"]["percentage"]["cached"]
        )
        self.memo_time_series.slices()[2].setValue(
            statdict["rsrcscreen"]["memo"]["percentage"]["used"]
        )
        self.swap_time_series.slices()[0].setValue(
            statdict["rsrcscreen"]["swap"]["percentage"]["free"]
        )
        self.swap_time_series.slices()[1].setValue(
            statdict["rsrcscreen"]["swap"]["percentage"]["used"]
        )
        self.memouspc.setText("%2.1f%%" % statdict["rsrcscreen"]["memo"]["percentage"]["used"])
        self.memoccpc.setText("%2.1f%%" % statdict["rsrcscreen"]["memo"]["percentage"]["cached"])
        self.memofrpc.setText("%2.1f%%" % statdict["rsrcscreen"]["memo"]["percentage"]["free"])
        self.memousnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["used"]))
        self.memoccnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["cached"]))
        self.memofrnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["free"]))
        self.memottnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["total"]))
        self.memoacnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["active"]))
        self.memobfnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["buffers"]))
        self.memoshnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["shared"]))
        self.memosbnm.setText("%s" % str(statdict["rsrcscreen"]["memo"]["absolute"]["slab"]))
        self.swapuspc.setText("%2.1f%%" % statdict["rsrcscreen"]["swap"]["percentage"]["used"])
        self.swapfrpc.setText("%2.1f%%" % statdict["rsrcscreen"]["swap"]["percentage"]["free"])
        self.swapusnm.setText("%s" % str(statdict["rsrcscreen"]["swap"]["absolute"]["used"]))
        self.swapfrnm.setText("%s" % str(statdict["rsrcscreen"]["swap"]["absolute"]["free"]))
        self.swapttnm.setText("%s" % str(statdict["rsrcscreen"]["swap"]["absolute"]["total"]))
        self.swapsinm.setText("%s" % str(statdict["rsrcscreen"]["swap"]["absolute"]["sin"]))
        self.swapsonm.setText("%s" % str(statdict["rsrcscreen"]["swap"]["absolute"]["sout"]))
        self.cpudcsnm.setText(str(statdict["rsrcscreen"]["cpud"]["absolute"]["ctx_switches"]))
        self.cpudinnm.setText(str(statdict["rsrcscreen"]["cpud"]["absolute"]["interrupts"]))
        self.cpudsinm.setText(str(statdict["rsrcscreen"]["cpud"]["absolute"]["soft_interrupts"]))
        self.cpudscnm.setText(str(statdict["rsrcscreen"]["cpud"]["absolute"]["sys_calls"]))

    def initialize_activities_tabscreen(self):
        self.proctree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.proctree.verticalHeader().setVisible(False)
        self.proctree.setColumnWidth(0, 75)
        self.proctree.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.proctree.setColumnWidth(2, 75)
        self.proctree.setColumnWidth(3, 125)
        self.proctree.setColumnWidth(4, 75)
        self.proctree.setColumnWidth(5, 75)
        self.proctree.setColumnWidth(6, 75)
        self.proctree.setColumnWidth(7, 75)
        self.cntbvers.setText("Version %s" % __version__)
        self.proctree.cellClicked.connect(self.open_process_window)
        self.ntwkrfrs.clicked.connect(self.initialize_connections_tabscreen)
        self.phptrfrs.clicked.connect(self.initialize_partitions_tabscreen)
        self.lgptrfrs.clicked.connect(self.initialize_partitions_tabscreen)

    def refresh_activities_tabscreen(self, statdict):
        self.procqant.setText("%d processes" % statdict["procscreen"]["process_count"])
        self.proctree.setRowCount(0)
        self.proctree.insertRow(0)
        self.proctree.verticalHeader().setDefaultSectionSize(20)
        for row, form in enumerate(statdict["procscreen"]["process_list"]):
            for column, item in enumerate(form):
                self.proctree.setItem(row, column, QTableWidgetItem(str(item)))
            self.proctree.insertRow(self.proctree.rowCount())
        self.proctree.setRowCount(self.proctree.rowCount() - 1)

    def initialize_performance_tabscreen(self):
        self.perflist.setSelectionMode(QAbstractItemView.NoSelection)
        cpuidict = tab_performance.return_cpu_specifications_information()
        featlist = tab_performance.return_feature_flags_information()
        self.cpuiname.setText(str(cpuidict["name"]))
        self.cpuivend.setText(str(cpuidict["vendor"]))
        self.cpuifreq.setText(str(cpuidict["frequency"]))
        self.cpuiqant.setText(str(cpuidict["count"]))
        self.cpuibits.setText(str(cpuidict["bits"]))
        self.cpuiarch.setText(str(cpuidict["arch"]))
        self.cpuistep.setText(str(cpuidict["stepping"]))
        self.cpuimodl.setText(str(cpuidict["model"]))
        self.cpuifmly.setText(str(cpuidict["family"]))
        for indx in featlist["featflag"]:
            self.fefllist.addItem(indx)
        self.perflist.clear()
        perfdict = tab_performance.return_mainscreen_threaded_statistics()
        self.perfname.setText("%d CPU(s)" % len(perfdict))
        for indx in perfdict.keys():
            listitem = QListWidgetItem(self.perflist)
            wdgtitem = PerfWdgt(
                self,
                indx + 1,
                perfdict[indx]["cputimes"],
                perfdict[indx]["cpuclock"],
            )
            listitem.setSizeHint(QSize(530, 275))
            self.perflist.setItemWidget(listitem, wdgtitem)
            self.perfwgls.append(wdgtitem)
            self.perflist.addItem(listitem)

    def refresh_performance_tabscreen(self, statdict):
        for indx in range(len(self.perfwgls)):
            self.perfwgls[indx].modify_attributes(
                indx + 1,
                statdict["perfscreen"][indx]["cputimes"],
                statdict["perfscreen"][indx]["cpuclock"],
            )

    def initialize_connections_tabscreen(self):
        self.ntwkwgls = []
        self.ntwklist.setSelectionMode(QAbstractItemView.NoSelection)
        self.ntwklist.clear()
        ntwkdict = tab_network.return_pernic_threaded_statistics()
        logging.warning("Network devices list was successfully updated")
        self.statusBar.showMessage(
            "[%s] Network devices list was successfully updated"
            % datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        )
        self.ntwkqant.setText("%d NIC(s)" % len(ntwkdict))
        for indx in range(len(ntwkdict)):
            listitem = QListWidgetItem(self.ntwklist)
            wdgtitem = NtwkWdgt(
                self,
                ntwkdict[indx][0],
                ntwkdict[indx][1],
                ntwkdict[indx][2],
                ntwkdict[indx][3],
                ntwkdict[indx][4],
                ntwkdict[indx][5],
                ntwkdict[indx][6],
                ntwkdict[indx][7],
                ntwkdict[indx][8],
                ntwkdict[indx][9],
                ntwkdict[indx][10],
                ntwkdict[indx][11],
                ntwkdict[indx][12],
                ntwkdict[indx][13],
            )
            listitem.setSizeHint(QSize(685, 120))
            self.ntwklist.setItemWidget(listitem, wdgtitem)
            self.ntwkwgls.append(wdgtitem)
            self.ntwklist.addItem(listitem)

    def refresh_connections_tabscreen(self, statdict):
        self.ntwkbrrt.setText(str(statdict["ntwkscreen"]["globrate"]["bytes"]["recv"]))
        self.ntwkbtrt.setText(str(statdict["ntwkscreen"]["globrate"]["bytes"]["sent"]))
        self.ntwkbrdt.setText(str(statdict["ntwkscreen"]["mainscrn"]["bytes"]["recv"]))
        self.ntwkbtdt.setText(str(statdict["ntwkscreen"]["mainscrn"]["bytes"]["sent"]))
        self.ntwkprrt.setText(str(statdict["ntwkscreen"]["globrate"]["packets"]["recv"]))
        self.ntwkptrt.setText(str(statdict["ntwkscreen"]["globrate"]["packets"]["sent"]))
        self.ntwkprdt.setText(str(statdict["ntwkscreen"]["mainscrn"]["packets"]["recv"]))
        self.ntwkptdt.setText(str(statdict["ntwkscreen"]["mainscrn"]["packets"]["sent"]))
        self.ntwkertx.setText(str(statdict["ntwkscreen"]["mainscrn"]["errors"]["recv"]))
        self.ntwkettx.setText(str(statdict["ntwkscreen"]["mainscrn"]["errors"]["sent"]))
        self.ntwkdrtx.setText(str(statdict["ntwkscreen"]["mainscrn"]["dropped"]["recv"]))
        self.ntwkdttx.setText(str(statdict["ntwkscreen"]["mainscrn"]["dropped"]["sent"]))
        try:
            for indx in range(len(self.ntwkwgls)):
                self.ntwkwgls[indx].modify_attributes(
                    statdict["ntwkscreen"]["pernicrt"][indx][0],
                    statdict["ntwkscreen"]["pernicrt"][indx][1],
                    statdict["ntwkscreen"]["pernicrt"][indx][2],
                    statdict["ntwkscreen"]["pernicrt"][indx][3],
                    statdict["ntwkscreen"]["pernicrt"][indx][4],
                    statdict["ntwkscreen"]["pernicrt"][indx][5],
                    statdict["ntwkscreen"]["pernicrt"][indx][6],
                    statdict["ntwkscreen"]["pernicrt"][indx][7],
                    statdict["ntwkscreen"]["pernicrt"][indx][8],
                    statdict["ntwkscreen"]["pernicrt"][indx][9],
                    statdict["ntwkscreen"]["pernicrt"][indx][10],
                    statdict["ntwkscreen"]["pernicrt"][indx][11],
                    statdict["ntwkscreen"]["pernicrt"][indx][12],
                    statdict["ntwkscreen"]["pernicrt"][indx][13],
                )
        except IndexError:
            logging.warning("A network device was just added or removed")
            logging.warning("Please click on the REFRESH button to obtain an updated list")
            self.statusBar.showMessage(
                "[%s] A network device was just added or removed - Please click on the REFRESH button to obtain an updated list"  # noqa
                % datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
            )

    def initialize_partitions_tabscreen(self):
        self.phptwgls, self.lgptwgls = [], []
        self.phptlist.setSelectionMode(QAbstractItemView.NoSelection)
        self.lgptlist.setSelectionMode(QAbstractItemView.NoSelection)
        self.phptlist.clear()
        self.lgptlist.clear()
        phptdict = tab_partitions.return_physical_partition_statistics()
        lgptdict = tab_partitions.return_logical_partition_statistics()
        logging.warning("Partitions list was successfully updated")
        self.statusBar.showMessage(
            "[%s] Partitions list was successfully updated"
            % datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        )
        self.partqant.setText("%d unit(s)" % (len(phptdict) + len(lgptdict)))
        self.phptstlb.setText("<b>Physical partitions</b> (%d units)" % len(phptdict))
        for indx in range(len(phptdict)):
            listitem = QListWidgetItem(self.phptlist)
            wdgtitem = PhPtWdgt(
                self,
                phptdict[indx]["phptdevc"],
                phptdict[indx]["phptfutl"],
                phptdict[indx]["phptfsys"],
            )
            listitem.setSizeHint(QSize(325, 115))
            self.phptlist.setItemWidget(listitem, wdgtitem)
            self.phptwgls.append(wdgtitem)
            self.phptlist.addItem(listitem)
        self.lgptstlb.setText("<b>Logical partitions</b> (%d units)" % len(lgptdict))
        for indx in range(len(lgptdict)):
            listitem = QListWidgetItem(self.lgptlist)
            wdgtitem = LgPtWdgt(
                self,
                lgptdict[indx]["lgptdevc"],
                lgptdict[indx]["lgptfutl"],
                lgptdict[indx]["lgptfsys"],
            )
            listitem.setSizeHint(QSize(325, 115))
            self.lgptlist.setItemWidget(listitem, wdgtitem)
            self.lgptwgls.append(wdgtitem)
            self.lgptlist.addItem(listitem)

    def refresh_partitions_tabscreen(self, statdict):
        self.partbrrt.setText(statdict["partscreen"]["counters"]["savebyte"])
        self.partbrdt.setText(statdict["partscreen"]["counters"]["savetime"])
        self.partbtrt.setText(statdict["partscreen"]["counters"]["loadbyte"])
        self.partbtdt.setText(statdict["partscreen"]["counters"]["loadtime"])
        self.partprrt.setText(str(statdict["partscreen"]["counters"]["saveqant"]))
        self.partprdt.setText(str(statdict["partscreen"]["counters"]["savemgqt"]))
        self.partptrt.setText(str(statdict["partscreen"]["counters"]["loadqant"]))
        self.partptdt.setText(str(statdict["partscreen"]["counters"]["loadmgqt"]))
        try:
            for indx in range(len(self.phptwgls)):
                self.phptwgls[indx].modify_attributes(
                    statdict["partscreen"]["phptdata"][indx]["phptdevc"],
                    statdict["partscreen"]["phptdata"][indx]["phptfutl"],
                    statdict["partscreen"]["phptdata"][indx]["phptfsys"],
                )
        except IndexError:
            logging.warning("A physical partition was just added or removed")
            logging.warning("Please click on the REFRESH button to obtain an updated list")
            self.statusBar.showMessage(
                "[%s] A physical partition was just added or removed - Please click on the REFRESH button to obtain an updated list"  # noqa
                % datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
            )
        try:
            for indx in range(len(self.lgptwgls)):
                self.lgptwgls[indx].modify_attributes(
                    statdict["partscreen"]["lgptdata"][indx]["lgptdevc"],
                    statdict["partscreen"]["lgptdata"][indx]["lgptfutl"],
                    statdict["partscreen"]["lgptdata"][indx]["lgptfsys"],
                )
        except IndexError:
            logging.warning("A logical partition was just added or removed")
            logging.warning("Please click on the REFRESH button to obtain an updated list")
            self.statusBar.showMessage(
                "[%s] A logical partition was just added or removed - Please click on the REFRESH button to obtain an updated list"  # noqa
                % datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
            )

    def initialize_information_tabscreen(self):
        softdict = tab_information.return_software_information()
        obsrdict = tab_information.return_obserware_information()
        self.softname.setText(str(softdict["name"]))
        self.softvers.setText(str(softdict["version"]))
        self.softhost.setText(str(softdict["hostname"]))
        self.softrlse.setText(str(softdict["release"]))
        self.softrend.setText(str(softdict["rendition"]))
        self.softboot.setText(str(softdict["boottime"]))
        self.obsrvers.setText(str(obsrdict["obsrvers"]))
        self.obsrpyth.setText(str(obsrdict["pythvers"]))
        self.obsrpyqt.setText(str(obsrdict["pyqtvers"]))
        self.obsrpsut.setText(str(obsrdict["psutvers"]))
        self.obsrcpui.setText(str(obsrdict["cpuivers"]))
        self.obsrdist.setText(str(obsrdict["distvers"]))
        self.softvrlb.setText("Obserware v%s" % str(obsrdict["obsrvers"]))

    def initialize_elements(self):
        self.initialize_bottombar_statistics()
        self.initialize_resources_tabscreen()
        self.initialize_activities_tabscreen()
        self.initialize_information_tabscreen()
        self.initialize_performance_tabscreen()
        self.initialize_connections_tabscreen()
        self.initialize_partitions_tabscreen()
        logging.warning("Obserware v%s is ready" % __version__)
        self.statusBar.showMessage(
            "[%s] Obserware v%s is ready"
            % (datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"), __version__)
        )

    def refresh_elements(self, statdict):
        self.refresh_bottombar_statistics(statdict)
        self.refresh_resources_tabscreen(statdict)
        self.refresh_activities_tabscreen(statdict)
        self.refresh_performance_tabscreen(statdict)
        self.refresh_connections_tabscreen(statdict)
        self.refresh_partitions_tabscreen(statdict)
