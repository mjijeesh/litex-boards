#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2020 Piotr Esden-Tempski <piotr@esden.net>
# SPDX-License-Identifier: BSD-2-Clause

# iCEBreaker FPGA:
# - Crowd Supply campaign: https://www.crowdsupply.com/1bitsquared/icebreaker
# - 1BitSquared Store: https://1bitsquared.com/products/icebreaker
# - Design files: https://github.com/icebreaker-fpga/icebreaker

from litex.build.generic_platform import *
from litex.build.microsemi import MicrosemiPlatform # Assuming creative board uses Microsemi
from litex.build.microsemi.programmer import FlashProExpressProgrammer

# IOs ----------------------------------------------------------------------------------------------
  

_io = [

       ("xtl",     0, Pins("AB21")),
       

       # SW1 Switch on board is reset input

       # SW1 and SW2 are active high input, SW1 is used as high reset input  for processor

       ("user_sw2", 0, Pins("U19"), IOStandard("LVCMOS33")),


       

       ("user_led",  0, Pins("AB18"), IOStandard("LVCMOS25")),
       ("user_led",  1, Pins("P1"), IOStandard("LVCMOS25")),
      

       ("DEVRESET_N" , 0, Pins("R15")),  #
       
       
       ("serial", 0,
        Subsignal("tx", Pins("H19")),
        Subsignal("rx", Pins("G18")),
        IOStandard("LVCMOS33"),
       ),


       # This is the actual serial connected to usb-uart, but d21 is not fabric i/o ??
       ("serial1", 0,
        Subsignal("tx", Pins("D21")),
        Subsignal("rx", Pins("C22")),
        IOStandard("LVCMOS33"),
       ),




       
       
       ("spiflash", 0,
        Subsignal("cs_n", Pins("N22")),
        Subsignal("clk", Pins("N19")),
        Subsignal("mosi", Pins("N21")),
        Subsignal("miso", Pins("N20")),
        IOStandard("LVCMOS33")
       ),
       
       




       # MII Ethernet
   
    ("eth_clocks", 0,
        Subsignal("tx", Pins("E2")),
        Subsignal("rx", Pins("G1")),
        IOStandard("LVCMOS33"),
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("1")),
        Subsignal("mdio",    Pins("J3")),
        Subsignal("mdc",     Pins("J4")),
        Subsignal("rx_dv",   Pins("H1")),
        Subsignal("rx_er",   Pins("J2")),
        Subsignal("tx_data", Pins("F3 E1 D1 D2")),
        Subsignal("tx_en",   Pins("F4")),
        Subsignal("rx_data", Pins("J1 H4 H5 G5")),
        Subsignal("col",     Pins("D3")),
        Subsignal("crs",     Pins("C1")),
        IOStandard("LVCMOS33"),
    ),   
   

       
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("PMOD1A", "4   2 47 45  3 48 46 44"),
    ("PMOD1B", "43 38 34 31 42 36 32 28"),
    ("PMOD2",  "27 25 21 19 26 23 20 18")
]


# Platform -----------------------------------------------------------------------------------------

class Platform(MicrosemiPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, device="M2S050-FG484-STD", toolchain="libero_soc"):
        
        MicrosemiPlatform.__init__(self, device, _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        """Create a programmer for this platform."""
        return FlashProExpressProgrammer(device=self.device)

    def do_finalize(self, fragment):
        MicrosemiPlatform.do_finalize(self, fragment)
        #self.add_period_constraint(self.lookup_request("clk50", loose=True), 1e9/50e6)
