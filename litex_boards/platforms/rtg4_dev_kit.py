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
#from litex.build.microsemi.programmer import FlashProExpressProgrammer

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
       
       ### This is spiflash0

       ("spiflash", 0,
        Subsignal("cs_n", Pins("C33")),
        Subsignal("clk",  Pins("C34")),
        Subsignal("mosi", Pins("H27")),
        Subsignal("miso", Pins("H28")),
        IOStandard("LVCMOS33")
       ),
       # separate resource for the WP  and Hold pin.
       ("spiflash_wp_n",   0, Pins("F30"), IOStandard("LVCMOS33")),    
       ("spiflash_hold_n", 0, Pins("C36"), IOStandard("LVCMOS33")),

       
       #swapping the mosi and miso pins for testing 
       ("spiflash_swap", 0,
        Subsignal("cs_n", Pins("J12")),
        Subsignal("clk", Pins("J14")),
        Subsignal("mosi", Pins("J13")),
        Subsignal("miso", Pins("K12")),
        IOStandard("LVCMOS33")
       ),
    
        ### This is spiflash1

       ("spiflash1", 0,
        Subsignal("cs_n", Pins("C39")),
        Subsignal("clk",  Pins("B39")),
        Subsignal("mosi", Pins("H31")),
        Subsignal("miso", Pins("H32")),
        IOStandard("LVCMOS33")
       ),


       # separate resource for the WP  and Hold pin.
       ("spiflash1_wp_n",   0, Pins("G34"), IOStandard("LVCMOS33")),    
       ("spiflash1_hold_n", 0, Pins("D36"), IOStandard("LVCMOS33")),
       
       
       ### not fixed so far
       ("spiflash4x", 0,
        Subsignal("cs_n", Pins("J12")),
        Subsignal("clk", Pins("J14")),
        Subsignal("dq", Pins("K12 J13 H14 G16")),        
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

    def create_programmer(self):
        """Create a programmer for this platform."""
        return FlashProExpressProgrammer(device=self.device)

    def do_finalize(self, fragment):
        MicrosemiPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50", loose=True), 1e9/50e6)

        ##  I/O Bank voltages for the board is specified here.
        self.toolchain.additional_io_constraints +=[
           
         "set_iobank  bank0 -vcci 1.5V -fixed yes ",  
         "set_iobank  bank1 -vcci 2.5V -fixed yes ", 
         "set_iobank  bank3 -vcci 3.3V -fixed yes ", 
         "set_iobank  bank4 -vcci 3.3V -fixed yes ", 
         "set_iobank  bank9 -vcci 1.5V -fixed yes ", 
        ]
        

