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
from litex.build.microsemi.programmer import LiberoProgrammer

# IOs ----------------------------------------------------------------------------------------------
  

_io = [

       ("clk50",     0, Pins("AA39"), IOStandard("LVCMOS25")),
       # SW1 Switch on board is reset input


       # SW1 and SW2 are active high input, SW1 is used as high reset input  for processor

       ("reset_n", 0, Pins("AA30"), IOStandard("LVCMOS25")),
       ("user_sw2", 0, Pins("AB31"), IOStandard("LVCMOS25")),


       #  same as the SW1  & SW@ , only for older projects which uses this name , remove later
       ("user_btn2", 0, Pins("H12"), IOStandard("LVCMOS25")),
       ("user_btn1", 0, Pins("H13"), IOStandard("LVCMOS25")),


       ("user_led",  0, Pins("W35"), IOStandard("LVCMOS25")),
       ("user_led",  1, Pins("W34"), IOStandard("LVCMOS25")),
       ("user_led",  2, Pins("V30"), IOStandard("LVCMOS25")),
       ("user_led",  3, Pins("W33"), IOStandard("LVCMOS25")),
       #("user_sw",   0, Pins("H12"), IOStandard("LVCMOS25")),
       #("user_sw",   1, Pins("H13"), IOStandard("LVCMOS25")),
       #("user_sw",   2, Pins("M15"),  IOStandard("LVCMOS25")),
       #("user_sw",   3, Pins("N15"),  IOStandard("LVCMOS25")),

       ("DEVRESET_N" , 0, Pins("M11")),  #
       
       ("serial", 0,
        Subsignal("tx", Pins("E28")),
        Subsignal("rx", Pins("E27")),
        IOStandard("LVCMOS33"),
       ),


       ("jtag", 0,
        Subsignal("tck", Pins("R14")),
        Subsignal("tms", Pins("N11")),
        Subsignal("tdo", Pins("P14")),
        Subsignal("tdi", Pins("P16")),
        Subsignal("trstb", Pins("N13")),
        
       ),
       
       # SPI0 On bank4 , 3.3V
       ("spiflash", 0,
        Subsignal("cs_n",  Pins("C33")),
        Subsignal("clk",   Pins("C34")),
        Subsignal("mosi",  Pins("H27")),
        Subsignal("miso",  Pins("H28")),
        #Subsignal("wp",    Pins("F30")),
        #Subsignal("reset", Pins("C36")),           
        IOStandard("LVCMOS33")
       ),
       # separate resource for the WP  and Hold pin.
       ("spiflash_wp_n",   0, Pins("F30"), IOStandard("LVCMOS33")),    
       ("spiflash_hold_n", 0, Pins("C36"), IOStandard("LVCMOS33")),
       
       ## SPI1 On bank4 , 3.3V
       ("spiflash2", 0,
        Subsignal("cs_n", Pins("B35")),
        Subsignal("clk",  Pins("B34")),
        Subsignal("mosi", Pins("E35")),
        Subsignal("miso", Pins("E36")),
        #Subsignal("wp",   Pins("G34")),
        #Subsignal("reset",Pins("D36")),
        IOStandard("LVCMOS33")
       ),
    
        
       
       
       
       
       
       ("axi_aclk_out", 0, Pins(1)),
       ("axi_arstn_out", 0, Pins(1)),
       
       ("axi",0,
        Subsignal('awvalid', Pins(1)),
        Subsignal('awready', Pins(1)),
        Subsignal('awaddr', Pins(32)),
        Subsignal('awprot', Pins(3)),
        Subsignal('wvalid', Pins(1)),
        Subsignal('wready', Pins(1)),
        Subsignal('wdata', Pins(32)),
        Subsignal('wstrb', Pins(4)),
        Subsignal('bvalid', Pins(1)),
        Subsignal('bready', Pins(1)),
        Subsignal('bresp', Pins(2)),
        Subsignal('arvalid', Pins(1)),
        Subsignal('arready', Pins(1)),
        Subsignal('araddr', Pins(32)),
        Subsignal('arprot', Pins(3)),
        Subsignal('rvalid', Pins(1)),
        Subsignal('rready', Pins(1)),
        Subsignal('rresp', Pins(2)),
        Subsignal('rdata', Pins(32)),
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

    def __init__(self, device="RT4G150_ES-CG1657M", toolchain="libero_soc"):
        
        MicrosemiPlatform.__init__(self, device, _io, _connectors, toolchain=toolchain)
        # Apply permanent Bank Voltage constraints for this board               
        # Clean standard LiteX style command injection
        self.add_platform_command("set_iobank Bank4 -vcci 3.30 -fixed true")
        self.add_platform_command("set_iobank Bank1 -vcci 2.50 -fixed true")
    
    # Intercept platform commands to feed your custom toolchain logic
    def add_platform_command(self, command, **kwargs):
        if "set_iobank" in command:
            self.toolchain.additional_iobank_constraints.append(command)
        else:
            super().add_platform_command(command, **kwargs)

    def create_programmer(self):
        """Create a programmer for this platform."""
        return LiberoProgrammer(build_dir=None, build_name=None)

    def do_finalize(self, fragment):
        MicrosemiPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", loose=True), 1e9/50e6)
    
