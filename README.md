# Micro Irritating Maze
This is a maze game played with tools using semiconductor chips before bonding. 
Specifically, the game is to use a 5um Tungsten Needle while looking into a semiconductor chip with a stereo microscope to go through a maze drawn with pads on the semiconductor chip.At this time, when the needle touches the maze wall, the LED for the crash judgment glows. 
![Operation Image](/images/system_fig.jpg)
![Layout](/images/klayout_fix.jpg)

## Purpose of Micro Irritating Maze
The purpose of creating this game is to destroy the conventional wisdom that this is how semiconductor design and manufacturing should be done. 
The Maker movement has created works that would not have been possible as product manufacturing until then, as the cost of 3D printers and PCB manufacturing has become cheaper. As a result, new possibilities were born there. 
I wanted to start this trend in semiconductors.

# System Configurations
As a semiconductor, it is a mixed analog-digital circuit that combines analog and digital circuits.  

## Digital Circuit
This digital circuit consists of two circuits: a circuit in which the walls of the maze are pads that count up when Needle touches them, and a circuit in which the timer starts when Needle touches the start pad (circle shape) and stops when Needle touches the goal pad (cross shape) to measure the time spent. The timer starts when the start pad is touched and stops when the goal pad is touched. 

## Analog Circuit
This analog circuit connects the various pads to the pins of the digital circuit section.  
When Needle touches each pad, it is connected to VSS, which allows each digital circuit pin to operate with a negative logic. 
![Xschem](/images/xschem.jpg)
![Pad&Regsiter Layout](/images/klayout_pad_reg.jpg)

The maze is automatically generated by the klayout plugin. 
[/klayout/maze2metal5_generater.py](klayout/maze2metal5_generater.py)
![Generated Maze Sample](/images/maze_sample.jpg)

## Mixed Analog-Digital Circuits
The final Layout was created by editing the digital circuit Layout generated by OpenLANE in Klayout to incorporate analog circuits such as mazes and pads. 
![Final Layout](/images/klayout_fix.jpg)

+ I want to create pads on the Metal5 layer, so we remove unnecessary VDD and VSS to make empty area. 
    ![OpenLANE Generated Digital Layout](/images/klayout_default.jpg)
    ![Delete Metal5 Layer Layout](/images/klayout_del_mel5.jpg)
+ Place the following pads on the Metal5 layer, which has an empty area, and perform the necessary wiring. 
    - Maze Wall Pad
        - This pad connect to Crash pin in Digital Circuit.
    - Start Pad
        - This pad connect to RST pin in Digital Circuit.
    - Goal Pad
        - This pad connect to Goal pin in Digital Circuit.
    - VDD Pad
        - This pad connect to VDD in Digital Circuit.
    - VSS Pad
        - This pad connect to VSS in Digital Circuit.
+ Since the Needle tip is 5um, the pad size was set to 800um. 
    ![5um Tungsten Needle](/images/needle_pen.png)
    ![Pad Explanation](/images/pad_exp.jpg)
+ Generate the maze. The path width of the maze was set at 300um. 
    ![Maze Explanation](/images/maze_exp.jpg)
+ Place pads and mazes on the layout and wire them to the digital circuit. 
    ![Conbine Pad&Regsiter&Digital Layout](/images/klayout_fix.jpg)

## Peripheral Systems
This semiconductor circuit does not work by itself. To work, you need an um-class Needle that you can buy at a home improvement store, a stereo microscope that costs tens of thousands of yen, and a power supply. 

- Stereo Microscope
    ![Stereo Microscope](/images/stereomicroscope.jpg)
- 5um Tungsten Needle
    ![5um Tungsten Needle](/images/needle_pen.png)
- Power Supply Unit
    ![Power Supply Unit](/images/kikusui_pmx.png)
- LED Circuit

![Operation Image](/images/system_fig.jpg)


### Files
- [/klayout/maze2metal5_generater.py](/klayout/maze2metal5_generater.py) 
    This is a plugin for Klayout that automatically generates mazes. 
    ![Generated Maze Sample](/images/maze_sample.jpg) 
- [/verilog/rtl/micro_irritating_maze.v](/verilog/rtl/micro_irritating_maze.v) 
    This is a digital circuit that measures the number of times the maze wall is hit and the time from the start of the maze to the goal. 
- [/gds/maze_Large.gds](/gds/maze_Large.gds) 
    This is a large maze with a road width of 300um. 
- [/gds/maze_Small.gds](/gds/maze_Small.gds)
    This is a small maze with a path width of 100um. It is used when a stereo microscope with high magnification is used. 
- [/gds/maze_Complex.gds](/gds/maze_Complex.gds) 
    This is a slightly complex shaped maze with a path width of 100um. It is used when a stereo microscope with high magnification is used. 
    ![Complex Maze](/images/maze_complex.jpg) 
- [/xschem/maze.sch](/xschem/maze.sch) 
    This is an analog circuit diagram for connecting the maze section to the digital circuit section. 
- [/gds/pad_and_resistor.gds](/gds/pad_and_resistor.gds)
    VDD pad, VSS pad and pad for pins for each maze operation.[/xschem/maze.sch](/xschem/maze.sch) is implemented. 
    Two types of pads are available: one for DIY probers (800um x 800um) and one for commercial probing systems (80um x 80um).

# Forked from the Caravel User Project

| :exclamation: Important Note            |
|-----------------------------------------|

## Caravel information follows

Refer to [README](docs/source/index.rst#section-quickstart) for a quickstart of how to use caravel_user_project

Refer to [README](docs/source/index.rst) for this sample project documentation. 

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![UPRJ_CI](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml) [![Caravel Build](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml)
