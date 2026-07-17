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

       ("clk50",     0, Pins("H16"), IOStandard("LVCMOS33")),
       # SW1 Switch on board is reset input


       # SW1 and SW2 are active high input, SW1 is used as high reset input  for processor

       ("user_sw1", 0, Pins("H12"), IOStandard("LVCMOS33")),
       ("user_sw2", 0, Pins("H13"), IOStandard("LVCMOS33")),


       #  same as the SW1  & SW@ , only for older projects which uses this name , remove later
       ("user_btn2", 0, Pins("H12"), IOStandard("LVCMOS33")),
       ("user_btn1", 0, Pins("H13"), IOStandard("LVCMOS33")),


       ("user_led",  0, Pins("J16"), IOStandard("LVCMOS33")),
       ("user_led",  1, Pins("K16"), IOStandard("LVCMOS33")),
       ("user_led",  2, Pins("M16"), IOStandard("LVCMOS33")),
       ("user_led",  3, Pins("N16"), IOStandard("LVCMOS33")),
       #("user_sw",   0, Pins("H12"), IOStandard("LVCMOS33")),
       #("user_sw",   1, Pins("H13"), IOStandard("LVCMOS33")),
       #("user_sw",   2, Pins("M15"),  IOStandard("LVCMOS33")),
       #("user_sw",   3, Pins("N15"),  IOStandard("LVCMOS33")),

      ("DEVRESET_N" , 0, Pins("M11") , Misc("reserved")),  #dedicated pin 
       
       ("serial", 0,
        Subsignal("tx", Pins("G3")),
        Subsignal("rx", Pins("H3")),
        IOStandard("LVCMOS33"),
       ),


       ("jtag", 0,
        Subsignal("tck", Pins("R14")),
        Subsignal("tms", Pins("N11")),
        Subsignal("tdo", Pins("P14")),
        Subsignal("tdi", Pins("P16")),
        Subsignal("trstb", Pins("N13")),
        
    ),
       
       
       ("spiflash", 0,
        Subsignal("cs_n", Pins("J12")),
        Subsignal("clk", Pins("J14")),
        Subsignal("mosi", Pins("K12")),
        Subsignal("miso", Pins("J13")),
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

       


       # --- Corrected DDR3 Definitions ---
    ("ddramold", 0,
        Subsignal("a",       Pins("C14 E11 E12 B16 C16 D16 E16 F15 F14 E15 E14 F13 D14 D13 C15 B15 ")),
        Subsignal("ba",      Pins("C12 D12 B13")),
        Subsignal("cas_n",   Pins("A12")),
        Subsignal("clk_p",   Pins("A14")),
        Subsignal("clk_n",   Pins("A15")),
        Subsignal("cke",     Pins("E10")),
        Subsignal("cs_n",    Pins("D11")),
        Subsignal("dm",      Pins("A3 C10")),
        Subsignal("dq",      Pins( "B2 A2 B6 B5 B3 B7 C6 A7 C8 C9 D7 D8 B11 B10 D9 E8")),
        Subsignal("dqs_p",   Pins("A5 A9")),
        Subsignal("dqs_n",   Pins("A4 A10")),
        Subsignal("odt",     Pins("F16")),
        Subsignal("ras_n",   Pins("B12")),
        Subsignal("reset_n", Pins("A13")),
        Subsignal("we_n",    Pins("C11")),
        Subsignal("dqs_tmatch_o",    Pins("A8")),
        Subsignal("dqs_tmatch_i",    Pins("B8")),

        

        IOStandard("SSTL18I"),
    ),

    ("ddram_shield", 0,
        Pins("AM22 AM20"),
        IOStandard("SHIELD15"),
    ),


    ### MDDR I/O are  dedicated pins, no need to specify the pin numbers here
    ("ddram", 0,
        Subsignal("a",       Pins(16)), # No pin numbers specified
        Subsignal("ba",      Pins(3)),
        Subsignal("cas_n",   Pins(1)),
        Subsignal("clk_p",   Pins(1)),
        Subsignal("clk_n",   Pins(1)),
        Subsignal("cke",     Pins(1)),
        Subsignal("cs_n",    Pins(1)),
        Subsignal("dm",      Pins(2)),
        Subsignal("dq",      Pins(16)),
        Subsignal("dqs_p",   Pins(2)),
        Subsignal("dqs_n",   Pins(2)),
        Subsignal("odt",     Pins(1)),
        Subsignal("ras_n",   Pins(1)),
        Subsignal("reset_n", Pins(1)),
        Subsignal("we_n",    Pins(1)),
        Subsignal("dqs_tmatch_o",   Pins(1)),
        Subsignal("dqs_tmatch_i",    Pins(1)),
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
    ("pmoda", "L12 L13 M13 N15 L11 L14 N14 M15"),
   
]

def sdcard_pmod_io(pmod):
            return [
                # SDCard PMOD:
                # - https://store.digilentinc.com/pmod-microsd-microsd-card-slot/
                ("spisdcard", 0,
                    Subsignal("clk",  Pins(f"{pmod}:3")),
                    Subsignal("mosi", Pins(f"{pmod}:1"), Misc("PULLUP ")),
                    Subsignal("cs_n", Pins(f"{pmod}:0"), Misc("PULLUP ")),
                    Subsignal("miso", Pins(f"{pmod}:2"), Misc("PULLUP ")),
                    IOStandard("LVCMOS33"),
                ),
                ("sdcard", 0,
                    Subsignal("data", Pins(f"{pmod}:2 {pmod}:4 {pmod}:5 {pmod}:0"), Misc("PULLUP")),
                    Subsignal("cmd",  Pins(f"{pmod}:1"), Misc("PULLUP")),
                    Subsignal("clk",  Pins(f"{pmod}:3")), 
                    Subsignal("cd",   Pins(f"{pmod}:6")),
                    IOStandard("LVCMOS33"),
                ),
]
_sdcard_pmod_io = sdcard_pmod_io("pmoda") # SDCARD PMOD on JA.



# Platform -----------------------------------------------------------------------------------------

class Platform(MicrosemiPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, device="M2S025-VF256", toolchain="libero_soc"):
        
        MicrosemiPlatform.__init__(self, device, _io, _connectors, toolchain=toolchain)
    
        # Add any IOBANK voltage settings here for the board .
        
        #self.add_platform_command("set_iobank Bank4 -vcci 3.30 -fixed true")
        #self.add_platform_command("set_iobank Bank1 -vcci 2.50 -fixed true")
    
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
    