#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2018-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.microsemi import MicrosemiPlatform
from litex.build.microsemi.programmer import  LiberoProgrammer

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
    ("spiflash_reset_n", 0, Pins("A24"), IOStandard("LVCMOS18")),
    
    ("spiflash4x", 0,
        Subsignal("clk",  Pins("H19")),
        Subsignal("cs_n", Pins("A20")),
        Subsignal("dq",   Pins("G19 C18 A27 A22")),
        IOStandard("LVCMOS18")
     
    ),

    
    ##### Below ports are not tested, needs to verify.
    
        
    # Fabric JTAG
    ("jtag", 0,
        Subsignal("tck",  Pins("KF8")),
        Subsignal("tms",  Pins("F7")),
        Subsignal("tdo",  Pins("F6")),
        Subsignal("tdi",  Pins("G8")),
        Subsignal("trstb", Pins("G7")),
        IOStandard("LVCMOS25")
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

    # --- Corrected DDR3 Definitions ---
    ("ddram", 0,
        Subsignal("a", Pins(
            "AL27 AL26 AM27 AN27 AN26 AP25 AL25 AK25 AJ23 AH23 "
            "AJ25 AJ24 AL22 AK23 AL24 AL23"
        )),
        Subsignal("ba",      Pins("AE25 AD23 AD25")),
        Subsignal("cas_n",   Pins("AF25")),
        Subsignal("clk_p",   Pins("AP26")),
        Subsignal("clk_n",   Pins("AP27")),
        Subsignal("cke",     Pins("AF22")),
        Subsignal("cs_n",    Pins("AE22")),
        Subsignal("dm",      Pins("AN23 AL20")),
        Subsignal("dq", Pins(
            "AN22 AN21 AM24 AN24 AP21 AP20 AP19 AN19 AM21 AK22 "
            "AK21 AK20 AJ20 AH21 AG21 AM19"
        )),
        Subsignal("dqs_p",   Pins("AP23 AH22")),
        Subsignal("dqs_n",   Pins("AP24 AJ21")),
        Subsignal("odt",     Pins("AF23")),
        Subsignal("ras_n",   Pins("AE23")),
        Subsignal("reset_n", Pins("AG22")),
        Subsignal("we_n",    Pins("AF24")),
        IOStandard("SSTL15II"),
    ),

    ("ddram_shield", 0,
        Pins("AM22 AM20"),
        IOStandard("SHIELD15"),
    ),
    
    

    

]

# Platform -----------------------------------------------------------------------------------------

class Platform(MicrosemiPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, device="MPF300T-1FCG1152I", toolchain="libero_soc"):
        MicrosemiPlatform.__init__(self, device, _io, toolchain=toolchain)
        
        # Add any IOBANK voltage settings here for the board .        
        self.add_platform_command("set_iobank -bank_name bank0 -vcci 1.2  -fixed true")
        self.add_platform_command("set_iobank -bank_name bank1 -vcci 1.5  -fixed true")
        #self.add_platform_command("set_iobank Bank2 -vcci 2.5  -fixed true")
        self.add_platform_command("set_iobank -bank_name Bank3 -vcci 2.5 -fixed true")
        self.add_platform_command("set_iobank -bank_name Bank6 -vcci 1.8 -fixed true")
    
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
        self.add_period_constraint(self.lookup_request("clk50", 0, loose=True), 1e9/50e6)
        
