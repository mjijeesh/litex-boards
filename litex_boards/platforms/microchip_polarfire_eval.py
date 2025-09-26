#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2018-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.microsemi import MicrosemiPlatform
from litex.build.microsemi.programmer import FlashProExpressProgrammer

# IOs ----------------------------------------------------------------------------------------------

   
    

_io = [
    # Clk / Rst
    ("clk50", 0, Pins("E25"), IOStandard("LVCMOS18")),
    ("reset_n", 0, Pins("K22"), IOStandard("LVCMOS18")),

    # Leds
    ("user_led", 0, Pins("F22"), IOStandard("LVCMOS18")),
    ("user_led", 1, Pins("B26"), IOStandard("LVCMOS18")),
    ("user_led", 2, Pins("C26"), IOStandard("LVCMOS18")),
    ("user_led", 3, Pins("D25"), IOStandard("LVCMOS18")),
    ("user_led", 4, Pins("C27"), IOStandard("LVCMOS18")),
    ("user_led", 5, Pins("F23"), IOStandard("LVCMOS18")),
    ("user_led", 6, Pins("H22"), IOStandard("LVCMOS18")),
    ("user_led", 7, Pins("H21"), IOStandard("LVCMOS18")),
       

    # Buttons
    ("user_btn", 0, Pins("H23"), IOStandard("LVCMOS18")),
    ("user_btn", 1, Pins("D21"), IOStandard("LVCMOS18")),
    ("user_btn", 2, Pins("H24"), IOStandard("LVCMOS18")),
    ("user_btn", 3, Pins("C22"), IOStandard("LVCMOS18")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("G17")),
        Subsignal("rx", Pins("H18")),
        IOStandard("LVCMOS18")
    ),
    
        
    # Fabric JTAG
    ("jtag", 0,
        Subsignal("tck",  Pins("KF8")),
        Subsignal("tms",  Pins("F7")),
        Subsignal("tdo",  Pins("F6")),
        Subsignal("tdi",  Pins("G8")),
        Subsignal("trstb", Pins("G7")),
        IOStandard("LVCMOS25")
    ),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("clk",  Pins("H19")),
        Subsignal("cs_n", Pins("A20")),
        Subsignal("mosi", Pins("G19")),
        Subsignal("miso", Pins("C18")),
        #Subsignal("wp",   Pins("A27")),  
        #Subsignal("hold", Pins("A22")), 
        IOStandard("LVCMOS18")
    ),
    
    # 2. A new, separate resource for the Write Protect pin.
    #    The "_n" suffix is a convention for active-low signals.
    ("spiflash_wp_n", 0, Pins("A27"), IOStandard("LVCMOS18")),

    # 3. A new, separate resource for the Hold pin.
    ("spiflash_hold_n", 0, Pins("A22"), IOStandard("LVCMOS18")),
    
    ("spiflash4x", 0,
        Subsignal("clk",  Pins("H19")),
        Subsignal("cs_n", Pins("A20")),
        Subsignal("dq",   Pins("G19 C18 A27 A22")),
        IOStandard("LVCMOS18")
     
    ),
    
    ("spiflash_dedicated", 0,
        Subsignal("clk",  Pins("G3")),
        Subsignal("cs_n", Pins("G4")),
        Subsignal("mosi", Pins("G5")),
        Subsignal("miso", Pins("G10")),
        # These connect to the FLASH and IFACE ports of the macro
        Subsignal("flash", Pins("H10")),
        Subsignal("iface", Pins("G9")),
        IOStandard("LVCMOS25") # Or the correct I/O standard
    ),

    # DDR3 SDRAM
    ("ddram", 0,
        Subsignal("a", Pins(
            "U5 U4  V4  W3 V5 W4  Y3 AA3",
            "Y4 Y5 AA2 AB2 V6 W6 AB3"),
            IOStandard("SSTL15II")),
        Subsignal("ba",    Pins("V7 Y6 U7"), IOStandard("SSTL15II")),
        Subsignal("ras_n", Pins("AA6"), IOStandard("SSTL15II")),
        Subsignal("cas_n", Pins("AA5"), IOStandard("SSTL15II")),
        Subsignal("we_n",  Pins("AB5"), IOStandard("SSTL15II")),
        Subsignal("cs_n",  Pins("W7"),  IOStandard("SSTL15II")),
        Subsignal("dm", Pins("Y9 R15"), IOStandard("SSTL15II")),
        Subsignal("dq", Pins(
            "T7   T8  U8 U9  R10  V9 V10 W9",
            "V14 U14 R12 T11 U15 T13 U13 T15"),
            IOStandard("SSTL15II")),
        Subsignal("dqs_p", Pins("T10 R13"), IOStandard("SSTL15II")),
        Subsignal("dqs_n", Pins("U10 T12"), IOStandard("SSTL15II")),
        Subsignal("clk_p", Pins("V2"), IOStandard("SSTL15II")),
        Subsignal("clk_n", Pins("W2"), IOStandard("SSTL15II")),
        Subsignal("cke", Pins("W8"),  IOStandard("SSTL15II")),
        Subsignal("odt", Pins("AA7"), IOStandard("SSTL15II")),
        Subsignal("reset_n", Pins("AB7"), IOStandard("SSTL15II")),
    ),

    # Ethernet
    ("eth_clocks", 0,
        Subsignal("tx", Pins("J8")),
        Subsignal("rx", Pins("K3")),
        IOStandard("LVCMOS18")
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("L8"), IOStandard("LVCMOS33")),
        Subsignal("int_n",   Pins("J4")),
        Subsignal("mdio",    Pins("H2")),
        Subsignal("mdc",     Pins("J2")),
        Subsignal("rx_ctl",  Pins("K5")),
        Subsignal("rx_data", Pins("J9 K1 K6 K4")),
        Subsignal("tx_ctl",  Pins("L5")),
        Subsignal("tx_data", Pins("K8 L1 L2 L3")),
        IOStandard("LVCMOS18")
    ),
    
    # ✅ AXI-Lite Master Interface (for internal connection, no pins assigned)
    ("axil_master", 0,
     # ✅ Add Clock and Active-Low Reset signals
        Subsignal("aclk",    Pins(1)),
        Subsignal("aresetn", Pins(1)),
     
        Subsignal("awaddr",  Pins(32)), # Just specify the width
        Subsignal("awvalid", Pins(1)),
        Subsignal("awready", Pins(1)),
        Subsignal("wdata",   Pins(32)),
        Subsignal("wstrb",   Pins(4)),
        Subsignal("wvalid",  Pins(1)),
        Subsignal("wready",  Pins(1)),
        Subsignal("bresp",   Pins(2)),
        Subsignal("bvalid",  Pins(1)),
        Subsignal("bready",  Pins(1)),
        Subsignal("araddr",  Pins(32)),
        Subsignal("arvalid", Pins(1)),
        Subsignal("arready", Pins(1)),
        Subsignal("rdata",   Pins(32)),
        Subsignal("rresp",   Pins(2)),
        Subsignal("rvalid",  Pins(1)),
        Subsignal("rready",  Pins(1)),
    ),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(MicrosemiPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, device="MPF300T-FCS1152I-1", toolchain="libero_soc"):
        MicrosemiPlatform.__init__(self, device, _io, toolchain=toolchain)
        
    def create_programmer(self):
        """Create a programmer for this platform."""
        return FlashProExpressProgrammer(device=self.device)

    def do_finalize(self, fragment):
        MicrosemiPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", 0, loose=True), 1e9/50e6)
        