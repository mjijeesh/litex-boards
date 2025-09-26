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
       ("user_led",  0, Pins("J16"), IOStandard("LVCMOS33")),
       ("user_led",  1, Pins("K16"), IOStandard("LVCMOS33")),
       ("user_led",  2, Pins("M16"), IOStandard("LVCMOS33")),
       ("user_led",  3, Pins("N16"), IOStandard("LVCMOS33")),
       #("user_sw",   0, Pins("H12"), IOStandard("LVCMOS33")),
       #("user_sw",   1, Pins("H13"), IOStandard("LVCMOS33")),
       #("user_sw",   2, Pins("M15"),  IOStandard("LVCMOS33")),
       #("user_sw",   3, Pins("N15"),  IOStandard("LVCMOS33")),
       
       ("serial", 0,
        Subsignal("tx", Pins("G3")),
        Subsignal("rx", Pins("H3")),
        IOStandard("LVCMOS33"),
       ),
       
       
       ("spiflash", 0,
        Subsignal("cs_n", Pins("J12")),
        Subsignal("clk", Pins("J14")),
        Subsignal("mosi", Pins("K12")),
        Subsignal("miso", Pins("J13")),
        IOStandard("LVCMOS33")
       ),
       
       #swapping the mosi and miso pins for testing 
       ("spiflash_swap", 0,
        Subsignal("cs_n", Pins("J12")),
        Subsignal("clk", Pins("J14")),
        Subsignal("mosi", Pins("J13")),
        Subsignal("miso", Pins("K12")),
        IOStandard("LVCMOS33")
       ),
    
        # separate resource for the WP  and Hold pin.
       ("spiflash_wp_n",   0, Pins("H14"), IOStandard("LVCMOS33")),    
       ("spiflash_hold_n", 0, Pins("G16"), IOStandard("LVCMOS33")),
       
       
       ("spiflash4x", 0,
        Subsignal("cs_n", Pins("J12")),
        Subsignal("clk", Pins("J14")),
        Subsignal("dq", Pins("K12 J13 H14 G16")),        
        IOStandard("LVCMOS33")        
       ),
       
       
       
       ("clk50",     0, Pins("H16"), IOStandard("LVCMOS33")),
       # SW1 Switch on board is reset input
       ("user_btn2", 0, Pins("H12"), IOStandard("LVCMOS33")),
       ("user_btn1", 0, Pins("H13"), IOStandard("LVCMOS33")), 
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

    def __init__(self, device="M2S025-VF256", toolchain="libero_soc"):
        
        MicrosemiPlatform.__init__(self, device, _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        """Create a programmer for this platform."""
        return FlashProExpressProgrammer(device=self.device)

    def do_finalize(self, fragment):
        MicrosemiPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", loose=True), 1e9/50e6)
