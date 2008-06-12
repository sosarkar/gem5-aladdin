# Copyright (c) 2008 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Gabe Black

from m5.params import *
from m5.proxy import *
from Uart import Uart8250
from Device import IsaFake
from SouthBridge import SouthBridge
from Platform import Platform
from Pci import PciConfigAll
from SimConsole import SimConsole

def x86IOAddress(port):
    IO_address_space_base = 0x8000000000000000
    return IO_address_space_base + port;

class PC(Platform):
    type = 'PC'
    system = Param.System(Parent.any, "system")

    pciconfig = PciConfigAll()

    south_bridge = SouthBridge()

    # "Non-existant" port used for timing purposes by the linux kernel
    i_dont_exist = IsaFake(pio_addr=x86IOAddress(0x80), pio_size=1)

    # Ports behind the pci config and data regsiters. These don't do anything,
    # but the linux kernel fiddles with them anway.
    behind_pci = IsaFake(pio_addr=x86IOAddress(0xcf8), pio_size=8)

    # Serial port and console
    console = SimConsole()
    com_1 = Uart8250()
    com_1.pio_addr = x86IOAddress(0x3f8)
    com_1.sim_console = console

    def attachIO(self, bus):
        self.south_bridge.pio = bus.port
        self.i_dont_exist.pio = bus.port
        self.behind_pci.pio = bus.port
        self.com_1.pio = bus.port
        self.pciconfig.pio = bus.default
        bus.responder_set = True
        bus.responder = self.pciconfig
