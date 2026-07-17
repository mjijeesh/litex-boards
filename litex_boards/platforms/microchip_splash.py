#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2018-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.microsemi import MicrosemiPlatform
from litex.build.microsemi.programmer import LiberoProgrammer

# IOs ----------------------------------------------------------------------------------------------

   
    

_io = [
    # Main Clock
    ("clk50", 0, Pins("H7"), IOStandard("LVCMOS33")),

    # System Reset
    ("reset_n", 0, Pins("N4"), IOStandard("LVCMOS33")),

    # Serial (UART)
    ("serial", 0,
        Subsignal("rx", Pins("R5"), IOStandard("LVCMOS33")),
        Subsignal("tx", Pins("R4"), IOStandard("LVCMOS33")),
    ),

    # User LEDs
    ("user_led", 0, Pins("P7"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("P8"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("N7"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("N8"), IOStandard("LVCMOS33")),
    ("user_led", 4, Pins("N6"), IOStandard("LVCMOS33")),
    ("user_led", 5, Pins("N5"), IOStandard("LVCMOS33")),
    ("user_led", 6, Pins("M8"), IOStandard("LVCMOS33")),
    ("user_led", 7, Pins("M9"), IOStandard("LVCMOS33")),

    # User Push Buttons
    ("user_sw", 0, Pins("L6"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("M7"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("K5"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("K4"), IOStandard("LVCMOS33")),

    # User DIP Switches
    ("user_dip_switch", 0, Pins("L3"), IOStandard("LVCMOS33")),
    ("user_dip_switch", 1, Pins("M4"), IOStandard("LVCMOS33")),
    ("user_dip_switch", 2, Pins("J6"), IOStandard("LVCMOS33")),
    ("user_dip_switch", 3, Pins("K6"), IOStandard("LVCMOS33")),

    # DDR4 SDRAM
    # Note: I/O standards for DDR4 are typically set by the IP Core.
    ("ddram_ref_clk", 0, Pins("H7"), IOStandard("LVCMOS33")), # Using main clk as ref clk
    
    ("ddram", 0,
        Subsignal("a",       Pins(
            "U5  U4  V4  W3  V5  W4  Y3  AA3",
            "Y4  Y5  AA2 AB2 V6  W6")),
        Subsignal("ba",      Pins("V7 Y6")),
        Subsignal("bg",      Pins("AA5")),
        Subsignal("ras_n",   Pins("U7")),
        Subsignal("cas_n",   Pins("AB4")),
        Subsignal("we_n",    Pins("AB3")),
        Subsignal("act_n",   Pins("AA6")),
        Subsignal("cs_n",    Pins("W7")),
        Subsignal("cke",     Pins("W8")),
        Subsignal("odt",     Pins("AA7")),
        Subsignal("reset_n", Pins("AB7")),
        Subsignal("clk_p",   Pins("V1")),
        Subsignal("clk_n",   Pins("W1")),
        Subsignal("dq",      Pins(
            "T7  T8  U8  U9  R10 V9  V10 W9",   # Byte 0
            "V14 U14 R12 T11 U15 T13 U13 T15",  # Byte 1
            "U12 V11 W11 Y10 V12 W12 Y11 AA11", # Byte 2
            "W13 Y13 AA13 AB13 AB15 W14 Y14 Y15"  # Byte 3
        )),
        Subsignal("dqs_p",   Pins("T10 R13 AB8 AA12")),
        Subsignal("dqs_n",   Pins("U10 T12 AB9 AB12")),
        Subsignal("dm_n",    Pins("Y9 R15 AA10 AA15")), # Mapped to DBI_N
    ),
    ("ddram_shield", 0,
        Subsignal("shield0", Pins("R9")),
        Subsignal("shield1", Pins("V15")),
        Subsignal("shield2", Pins("AB10")),
        Subsignal("shield3", Pins("AB14")),
    ),

    # DDR4 Debug/Status LEDs (optional)
    ("ddr4_ctrl_ready", 0, Pins("B14"), IOStandard("LVCMOS33")),
    ("ddr4_pll_lock",   0, Pins("B15"), IOStandard("LVCMOS33")),

    # PCIe (x4)
    ("pcie_x4", 0,
        Subsignal("clk_p", Pins("R19")),
        Subsignal("clk_n", Pins("R20")),
        Subsignal("rx_p",  Pins("M22 T22 W20 AA20")),
        Subsignal("rx_n",  Pins("M21 T21 W19 AA19")),
        Subsignal("tx_p",  Pins("P22 V22 Y22 AB22")),
        Subsignal("tx_n",  Pins("P21 V21 Y21 AB21")),
        Subsignal("rst_n", Pins("T3"), IOStandard("LVCMOS33")),
    ),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(MicrosemiPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, toolchain="libero_soc"):
        MicrosemiPlatform.__init__(self, "MPF300T_ES-1FCG484EXT", _io, toolchain=toolchain)
        
    def create_programmer(self):
        """Create a programmer for this platform."""
        return LiberoProgrammer(build_dir=None, build_name=None)

    def do_finalize(self, fragment):
        MicrosemiPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", 0, loose=True), 1e9/50e6)
        