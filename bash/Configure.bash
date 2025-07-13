#!/bin/bash

# ConfigureInit + SPID

devmem 0x43c00000 32 0x00000003 # turn on all leds
devmem 0x43c00000 32 0x0003000f # PI bank disable
devmem 0x43c00000 32 0x00030003 # PI bank enable bank 3
devmem 0x43c00000 32 0x00020000 # j1 ref = 0
devmem 0x43c00000 32 0x00040200 # PI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00050200 # PI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00060200 # PI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x000704ec # PI bank 3 freq divider
devmem 0x43c00000 32 0x0008000f # PD bank disable 
devmem 0x43c00000 32 0x00080003 # PD bank enable 3
devmem 0x43c00000 32 0x00090200 # PD bank 0 freq divider - disabled
devmem 0x43c00000 32 0x000a0200 # PD bank 1 freq divider - disabled
devmem 0x43c00000 32 0x000b0200 # PD bank 2 freq divider - disabled
devmem 0x43c00000 32 0x000c0200 # PD bank 3 freq divider
devmem 0x43c00000 32 0x00120000 # spike expansor reset
devmem 0x43c00000 32 0x001209C4 # spike expansor set
devmem 0x43c00000 32 0x0013000f # EI bank disable
devmem 0x43c00000 32 0x00130003 # EI bank enable bank 3
devmem 0x43c00000 32 0x00140200 # EI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00150200 # EI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00160200 # EI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00170008 # EI bank 3 freq divider
devmem 0x43c00000 32 0x00000000 # turn off all leds
devmem 0x43c00000 32 0x00020000 # j1 ref = 0

devmem 0x43c00000 32 0x00200003 # turn on all leds
devmem 0x43c00000 32 0x0023000f # PI bank disable
devmem 0x43c00000 32 0x00230003 # PI bank enable bank 3
devmem 0x43c00000 32 0x00220000 # j2 ref = 0
devmem 0x43c00000 32 0x00240200 # PI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00250200 # PI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00260200 # PI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x002704ec # PI bank 3 freq divider
devmem 0x43c00000 32 0x0028000f # PD bank disable 
devmem 0x43c00000 32 0x00280003 # PD bank enable 3
devmem 0x43c00000 32 0x00290200 # PD bank 0 freq divider - disabled
devmem 0x43c00000 32 0x002a0200 # PD bank 1 freq divider - disabled
devmem 0x43c00000 32 0x002b0200 # PD bank 2 freq divider - disabled
devmem 0x43c00000 32 0x002c0200 # PD bank 3 freq divider
devmem 0x43c00000 32 0x00320000 # spike expansor reset
devmem 0x43c00000 32 0x003209C4 # spike expansor set
devmem 0x43c00000 32 0x0033000f # EI bank disable
devmem 0x43c00000 32 0x00330003 # EI bank enable bank 3
devmem 0x43c00000 32 0x00340200 # EI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00350200 # EI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00360200 # EI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00370008 # EI bank 3 freq divider
devmem 0x43c00000 32 0x00200000 # turn off all leds
devmem 0x43c00000 32 0x00220000 # j2 ref = 0

devmem 0x43c00000 32 0x00400003 # turn on all leds
devmem 0x43c00000 32 0x0043000f # PI bank disable
devmem 0x43c00000 32 0x00430003 # PI bank enable bank 3
devmem 0x43c00000 32 0x00420000 # j3 ref = 0
devmem 0x43c00000 32 0x00440200 # PI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00450200 # PI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00460200 # PI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x004704ec # PI bank 3 freq divider
devmem 0x43c00000 32 0x0048000f # PD bank disable 
devmem 0x43c00000 32 0x00480003 # PD bank enable 3
devmem 0x43c00000 32 0x00490200 # PD bank 0 freq divider - disabled
devmem 0x43c00000 32 0x004a0200 # PD bank 1 freq divider - disabled
devmem 0x43c00000 32 0x004b0200 # PD bank 2 freq divider - disabled
devmem 0x43c00000 32 0x004c0200 # PD bank 3 freq divider
devmem 0x43c00000 32 0x00520000 # spike expansor reset
devmem 0x43c00000 32 0x005209C4 # spike expansor set
devmem 0x43c00000 32 0x0053000f # EI bank disable
devmem 0x43c00000 32 0x00530003 # EI bank enable bank 3
devmem 0x43c00000 32 0x00540200 # EI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00550200 # EI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00560200 # EI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00570008 # EI bank 3 freq divider
devmem 0x43c00000 32 0x00400000 # turn off all leds
devmem 0x43c00000 32 0x00420000 # j3 ref = 0

devmem 0x43c00000 32 0x00600003 # turn on all leds
devmem 0x43c00000 32 0x0063000f # PI bank disable
devmem 0x43c00000 32 0x00630003 # PI bank enable bank 3
devmem 0x43c00000 32 0x00620000 # j4 ref = 0
devmem 0x43c00000 32 0x00640200 # PI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00650200 # PI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00660200 # PI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x006704ec # PI bank 3 freq divider
devmem 0x43c00000 32 0x0068000f # PD bank disable 
devmem 0x43c00000 32 0x00680003 # PD bank enable 3
devmem 0x43c00000 32 0x00690200 # PD bank 0 freq divider - disabled
devmem 0x43c00000 32 0x006a0200 # PD bank 1 freq divider - disabled
devmem 0x43c00000 32 0x006b0200 # PD bank 2 freq divider - disabled
devmem 0x43c00000 32 0x006c0200 # PD bank 3 freq divider
devmem 0x43c00000 32 0x00720000 # spike expansor reset
devmem 0x43c00000 32 0x007209C4 # spike expansor set
devmem 0x43c00000 32 0x0073000f # EI bank disable
devmem 0x43c00000 32 0x00730003 # EI bank enable bank 3
devmem 0x43c00000 32 0x00740200 # EI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00750200 # EI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00760200 # EI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00770008 # EI bank 3 freq divider
devmem 0x43c00000 32 0x00600000 # turn off all leds
devmem 0x43c00000 32 0x00620000 # j4 ref = 0

devmem 0x43c00000 32 0x00800003 # turn on all leds
devmem 0x43c00000 32 0x0083000f # PI bank disable
devmem 0x43c00000 32 0x00830003 # PI bank enable bank 3
devmem 0x43c00000 32 0x00820000 # j5 ref = 0
devmem 0x43c00000 32 0x00840200 # PI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00850200 # PI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00860200 # PI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x008704ec # PI bank 3 freq divider
devmem 0x43c00000 32 0x0088000f # PD bank disable 
devmem 0x43c00000 32 0x00880003 # PD bank enable 3
devmem 0x43c00000 32 0x00890200 # PD bank 0 freq divider - disabled
devmem 0x43c00000 32 0x008a0200 # PD bank 1 freq divider - disabled
devmem 0x43c00000 32 0x008b0200 # PD bank 2 freq divider - disabled
devmem 0x43c00000 32 0x008c0200 # PD bank 3 freq divider
devmem 0x43c00000 32 0x00920000 # spike expansor reset
devmem 0x43c00000 32 0x009209C4 # spike expansor set
devmem 0x43c00000 32 0x0093000f # EI bank disable
devmem 0x43c00000 32 0x00930003 # EI bank enable bank 3
devmem 0x43c00000 32 0x00940200 # EI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00950200 # EI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00960200 # EI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00970008 # EI bank 3 freq divider
devmem 0x43c00000 32 0x00800000 # turn off all leds
devmem 0x43c00000 32 0x00820000 # j5 ref = 0

devmem 0x43c00000 32 0x00a00003 # turn on all leds
devmem 0x43c00000 32 0x00a3000f # PI bank disable
devmem 0x43c00000 32 0x00a30003 # PI bank enable bank 3
devmem 0x43c00000 32 0x00a20000 # j6 ref = 0
devmem 0x43c00000 32 0x00a40200 # PI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00a50200 # PI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00a60200 # PI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00a704ec # PI bank 3 freq divider
devmem 0x43c00000 32 0x00a8000f # PD bank disable 
devmem 0x43c00000 32 0x00a80003 # PD bank enable 3
devmem 0x43c00000 32 0x00a90200 # PD bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00aa0200 # PD bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00ab0200 # PD bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00ac0200 # PD bank 3 freq divider
devmem 0x43c00000 32 0x00b20000 # spike expansor reset
devmem 0x43c00000 32 0x00b209C4 # spike expansor set
devmem 0x43c00000 32 0x00b3000f # EI bank disable
devmem 0x43c00000 32 0x00b30003 # EI bank enable bank 3
devmem 0x43c00000 32 0x00b40200 # EI bank 0 freq divider - disabled
devmem 0x43c00000 32 0x00b50200 # EI bank 1 freq divider - disabled
devmem 0x43c00000 32 0x00b60200 # EI bank 2 freq divider - disabled
devmem 0x43c00000 32 0x00b70008 # EI bank 3 freq divider
devmem 0x43c00000 32 0x00a00000 # turn off all leds
devmem 0x43c00000 32 0x00a20000 # j6 ref = 0