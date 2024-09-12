# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import subprocess
import time

import Qemu
import util

def test_huge_resource_vm():
    """
    Test huge resources  (Intel Case ID 007)
    """

    # choose half available memory per Intel case spec
    huge_mem_gb = int(util.get_memory_free_gb() / 2)
    num_cpus = int(util.get_num_cpus() / 2)

    qm = Qemu.QemuMachine()
    qm.qcmd.plugins['cpu'].nb_cores = num_cpus
    qm.qcmd.plugins['memory'].memory = '%dG' % (huge_mem_gb)
    qm.run()

    mon = Qemu.QemuMonitor(qm)
    mon.wait_for_state('running')

    qm.stop()


def test_max_vcpus():
    """
    Test max vcpus (No Intel Case ID)
    """
    num_cpus = util.get_num_cpus()
    if num_cpus > 255:
        num_cpus = 255 # max possible right now

    qm = Qemu.QemuMachine()
    qm.qcmd.plugins['cpu'].nb_cores = num_cpus
    qm.run()

    mon = Qemu.QemuMonitor(qm)
    mon.wait_for_state('running')

    qm.stop()


def test_max_guests():
    """
    Test max guests (No Intel Case ID)
    """

    # get max number of TD VMs we can create (max - current)
    max_td_vms = util.get_max_td_vms() - util.get_current_td_vms()
    qm = [None] * max_td_vms

    # initialize machines
    for i in range(max_td_vms):
        qm[i] = Qemu.QemuMachine()

    # start machines
    for i in range(max_td_vms):
        print("Starting machine %d" % (i))
        qm[i].run()

    # wait for all machines running
    for i in range(max_td_vms):
        print("Waiting for machine %d" % (i))
        mon = Qemu.QemuMonitor(qm[i])
        mon.wait_for_state('running')

    # stop all machines
    for i in range(max_td_vms):
        print("Stopping machine %d" % (i))
        qm[i].stop()

