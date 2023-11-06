v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 280 -80 280 -40 {
lab=VSS}
N 220 -380 220 -360 {
lab=VDD}
N 200 -280 240 -280 {
lab=GPIO_Crash}
N 580 -380 580 -360 {
lab=VDD}
N 560 -280 600 -280 {
lab=Maze_Start_Pad}
N 580 -300 580 -280 {
lab=Maze_Start_Pad}
N 220 -300 220 -280 {
lab=GPIO_Crash}
N 940 -380 940 -360 {
lab=VDD}
N 920 -280 960 -280 {
lab=Maze_Goal_Pad}
N 940 -300 940 -280 {
lab=Maze_Goal_Pad}
C {devices/vdd.sym} 220 -380 0 0 {name=l1 lab=VDD}
C {devices/gnd.sym} 280 -40 0 0 {name=l2 lab=VSS}
C {devices/opin.sym} 240 -280 0 0 {name=p1 lab=GPIO_Crash}
C {devices/ipin.sym} 560 -280 0 0 {name=p2 lab=Maze_Start_Pad}
C {devices/ipin.sym} 200 -280 0 0 {name=p3 lab=Maze_Wall_Pads}
C {devices/ipin.sym} 920 -280 0 0 {name=p4 lab=Maze_Goal_Pad}
C {devices/opin.sym} 600 -280 0 0 {name=p5 lab=GPIO_Goal}
C {devices/opin.sym} 960 -280 0 0 {name=p6 lab=GPIO_RST}
C {devices/res.sym} 220 -330 0 0 {name=R1
value=10k
footprint=1206
device=resistor
m=1}
C {devices/ipin.sym} 280 -80 0 0 {name=p7 lab=Irritating_Stick_Pad}
C {devices/vdd.sym} 580 -380 0 0 {name=l3 lab=VDD}
C {devices/res.sym} 580 -330 0 0 {name=R2
value=10k
footprint=1206
device=resistor
m=1}
C {devices/vdd.sym} 940 -380 0 0 {name=l4 lab=VDD}
C {devices/res.sym} 940 -330 0 0 {name=R3
value=10k
footprint=1206
device=resistor
m=1}
