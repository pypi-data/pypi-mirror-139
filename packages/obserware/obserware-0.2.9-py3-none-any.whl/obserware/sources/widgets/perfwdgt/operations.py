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


from PyQt5.QtChart import QChart, QPieSeries
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

from obserware.sources.widgets.perfwdgt.interface import Ui_perfwdgt


class PerfWdgt(QWidget, Ui_perfwdgt):
    def __init__(
        self,
        parent=None,
        cputnumb="0",
        cputimes={
            "time": {
                "cputusnm": 0,
                "cputuspr": 0,
                "cputkrnm": 0,
                "cputnull": 0,
                "cputiowt": 0,
                "cputhirq": 0,
                "cputsirq": 0,
                "cputvirt": 0,
                "cputgest": 0,
                "cputgtnc": 0,
            },
            "perc": {
                "cputusnm": 0,
                "cputuspr": 0,
                "cputkrnm": 0,
                "cputnull": 0,
                "cputiowt": 0,
                "cputhirq": 0,
                "cputsirq": 0,
                "cputvirt": 0,
                "cputgest": 0,
                "cputgtnc": 0,
            },
        },
        cpuclock={
            "usejperc": 0,
            "cpudhrtz": {
                "cpumaxhz": 0,
                "cpuminhz": 0,
                "cpucurhz": 0,
            },
        },
    ):
        super(PerfWdgt, self).__init__(parent)
        self.setupUi(self)
        self.cpuugraf = QChart()
        self.cpuutime = QPieSeries()
        self.handle_elements(cputnumb, cputimes, cpuclock)

    def handle_elements(self, cputnumb, cputimes, cpuclock):
        self.cputnumb.setText("%d" % cputnumb)
        self.cpuutime.setHoleSize(0.55)
        self.cpuugraf.setBackgroundBrush(QColor("transparent"))
        self.cpuufrlc = self.cpuutime.append("Free", 100 - cpuclock["usejperc"])
        self.cpuuuslc = self.cpuutime.append("Used", cpuclock["usejperc"])
        self.cpuugraf.legend().hide()
        self.cpuugraf.addSeries(self.cpuutime)
        self.cpuugraf.setAnimationOptions(QChart.SeriesAnimations)
        self.cpuugraf.setContentsMargins(-35, -35, -35, -35)
        self.cyclgraf.setChart(self.cpuugraf)
        self.cyclgraf.setRenderHint(QPainter.Antialiasing)
        self.cyclperc.setText("%d" % cpuclock["usejperc"])
        self.cyclcurt.setText("%s" % cpuclock["cpudhrtz"]["cpucurhz"])
        self.cyclxtra.setText(
            "<b>MIN:</b> %s, <b>MAX:</b> %s"
            % (cpuclock["cpudhrtz"]["cpuminhz"], cpuclock["cpudhrtz"]["cpumaxhz"])
        )
        self.cputusnm.setText(
            "<b>Executing normal processes in user mode:</b> %s (%d%%)"
            % (cputimes["time"]["cputusnm"], cputimes["perc"]["cputusnm"])
        )
        self.cputuspr.setText(
            "<b>Executing prioritized processes in user mode:</b> %s (%d%%)"
            % (cputimes["time"]["cputuspr"], cputimes["perc"]["cputuspr"])
        )
        self.cputkrnm.setText(
            "<b>Executing processes in kernel mode:</b> %s (%d%%)"
            % (cputimes["time"]["cputkrnm"], cputimes["perc"]["cputkrnm"])
        )
        self.cputnull.setText(
            "<b>Doing absolutely nothing:</b> %s (%d%%)"
            % (cputimes["time"]["cputnull"], cputimes["perc"]["cputnull"])
        )
        self.cputiowt.setText(
            "<b>Waiting for I/O operations to complete:</b> %s (%d%%)"
            % (cputimes["time"]["cputiowt"], cputimes["perc"]["cputiowt"])
        )
        self.cputhirq.setText(
            "<b>Servicing hardware interrupts:</b> %s (%d%%)"
            % (cputimes["time"]["cputhirq"], cputimes["perc"]["cputhirq"])
        )
        self.cputsirq.setText(
            "<b>Servicing software interrupts:</b> %s (%d%%)"
            % (cputimes["time"]["cputsirq"], cputimes["perc"]["cputsirq"])
        )
        self.cputvirt.setText(
            "<b>Running other OSes in a virtualized environment:</b> %s (%d%%)"
            % (cputimes["time"]["cputvirt"], cputimes["perc"]["cputvirt"])
        )
        self.cputgest.setText(
            "<b>Running a normal virtual CPU for guest OS on Linux kernel:</b> %s (%d%%)"
            % (cputimes["time"]["cputgest"], cputimes["perc"]["cputgest"])
        )
        self.cputgtnc.setText(
            "<b>Running a prioritized virtual CPU for guest OS on Linux kernel:</b> %s (%d%%)"
            % (cputimes["time"]["cputgtnc"], cputimes["perc"]["cputgtnc"])
        )

    def modify_attributes(self, cputnumb, cputimes, cpuclock):
        self.cyclperc.setText("%d" % cpuclock["usejperc"])
        self.cpuutime.slices()[0].setValue(100 - cpuclock["usejperc"])
        self.cpuutime.slices()[1].setValue(cpuclock["usejperc"])
        self.cyclcurt.setText("%s" % cpuclock["cpudhrtz"]["cpucurhz"])
        self.cyclxtra.setText(
            "<b>MIN:</b> %s, <b>MAX:</b> %s"
            % (cpuclock["cpudhrtz"]["cpuminhz"], cpuclock["cpudhrtz"]["cpumaxhz"])
        )
        self.cputusnm.setText(
            "<b>Executing normal processes in user mode:</b> %s (%d%%)"
            % (cputimes["time"]["cputusnm"], cputimes["perc"]["cputusnm"])
        )
        self.cputuspr.setText(
            "<b>Executing prioritized processes in user mode:</b> %s (%d%%)"
            % (cputimes["time"]["cputuspr"], cputimes["perc"]["cputuspr"])
        )
        self.cputkrnm.setText(
            "<b>Executing processes in kernel mode:</b> %s (%d%%)"
            % (cputimes["time"]["cputkrnm"], cputimes["perc"]["cputkrnm"])
        )
        self.cputnull.setText(
            "<b>Doing absolutely nothing:</b> %s (%d%%)"
            % (cputimes["time"]["cputnull"], cputimes["perc"]["cputnull"])
        )
        self.cputiowt.setText(
            "<b>Waiting for I/O operations to complete:</b> %s (%d%%)"
            % (cputimes["time"]["cputiowt"], cputimes["perc"]["cputiowt"])
        )
        self.cputhirq.setText(
            "<b>Servicing hardware interrupts:</b> %s (%d%%)"
            % (cputimes["time"]["cputhirq"], cputimes["perc"]["cputhirq"])
        )
        self.cputsirq.setText(
            "<b>Servicing software interrupts:</b> %s (%d%%)"
            % (cputimes["time"]["cputsirq"], cputimes["perc"]["cputsirq"])
        )
        self.cputvirt.setText(
            "<b>Running other OSes in a virtualized environment:</b> %s (%d%%)"
            % (cputimes["time"]["cputvirt"], cputimes["perc"]["cputvirt"])
        )
        self.cputgest.setText(
            "<b>Running a normal virtual CPU for guest OS on Linux kernel:</b> %s (%d%%)"
            % (cputimes["time"]["cputgest"], cputimes["perc"]["cputgest"])
        )
        self.cputgtnc.setText(
            "<b>Running a prioritized virtual CPU for guest OS on Linux kernel:</b> %s (%d%%)"
            % (cputimes["time"]["cputgtnc"], cputimes["perc"]["cputgtnc"])
        )
