// SPDX-FileCopyrightText: 2020 Efabless Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// SPDX-License-Identifier: Apache-2.0

`default_nettype none

module micro_irritating_maze #(
    parameter BITS = 16
)(
`ifdef USE_POWER_PINS
    inout vdd,	// User area 1 1.8V supply
    inout vss,	// User area 1 digital ground
`endif

    // Wishbone Slave ports (WB MI A)
    input wb_clk_i,
    input wb_rst_i,
    input wbs_stb_i,
    input wbs_cyc_i,
    input wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output wbs_ack_o,
    output [31:0] wbs_dat_o,

    // Logic Analyzer Signals
    input  [63:0] la_data_in,
    output [63:0] la_data_out,
    input  [63:0] la_oenb,

    // IOs
    input  [31:0] io_in,
    output [31:0] io_out,
    output [31:0] io_oeb,

);
    wire clk;
    wire rst;
    wire reset_out;
    wire crash;
    wire goal;

    wire [27:0] rdata; 
    wire [31:0] wdata;
    wire [7:0] crash_count;
    wire [19:0] timer_count;

    wire valid;
    wire [3:0] wstrb;
    wire [31:0] la_write;

    // WB MI A
    assign valid = wbs_cyc_i && wbs_stb_i; 
    assign wstrb = wbs_sel_i & {4{wbs_we_i}};
    assign wbs_dat_o =  {{(32-27){1'b0}}, rdata};
    assign wdata = wbs_dat_i[31:0];

    // IO
    assign io_out[27]  = rst;
    assign io_out[28]  = reset_out;
    assign io_out[29]  = clk;
    assign io_out[30]  = crash;
    assign io_out[31]  = goal;
    assign io_oeb[27] = 1'b0;
    assign io_oeb[28] = 1'b0;
    assign io_oeb[29] = 1'b0;
    assign io_oeb[30] = 1'b0;
    assign io_oeb[31] = 1'b0;
    assign io_out[19:0] = timer_count[19:0];
    assign io_out[26:20] = crash_count[6:0];
    assign io_oeb[19:0] = 0;
    assign io_oeb[26:20] = 0;

    // LA
    assign la_data_out = {{{(64-28){1'b0}}, timer_count[19:0]}, crash_count[7:0]};
    // Assuming LA probes [61:30] are for controlling the count register  
    assign la_write = ~la_oenb[61:62-BITS] & ~{BITS{valid}};
    // Assuming LA probes [63:62] are for controlling the count clk & reset  
    assign clk = (~la_oenb[62]) ? la_data_in[62]: wb_clk_i;
    assign rst = (~la_oenb[63]) ? la_data_in[63]: wb_rst_i;

    // From Maze Pads
    assign crash = 0;
    assign goal = 0;

    maze_counter #(
        .BITS(28)
    ) maze_counter(
        .clk(clk),
        .stop(goal),
        .crash_clk(crash),
        .reset(rst),
        .reset_out(reset_out),
        .ready(wbs_ack_o),
        .valid(valid),
        .rdata(rdata[27:0]),
        .wdata(wbs_dat_i[27:0]),
        .wstrb(wstrb),
        .la_write(la_write[27:0]),
        .la_input(la_data_in[27:0]),
        .crash_count(crash_count[7:0]),
        .timer_count(timer_count[19:0])
    );

endmodule

module maze_counter #(
    parameter BITS = 28
)(
    input clk,
    input stop,
    input crash_clk,
    input reset,
    input valid,
    input [3:0] wstrb,
    input [BITS-1:0] wdata,
    input [BITS-1:0] la_write,
    input [BITS-1:0] la_input,
    output ready,
    output reset_out,
    output [BITS-1:0] rdata,
    output [7:0] crash_count,
    output [19:0] timer_count
);
    reg ready;
    reg reset_out;
    reg wait_next_reset = 0;
    reg [15:0] clk_count = 0;

    reg [BITS-1:0] count;
    reg [BITS-1:0] rdata;

    reg [7:0] crash_count = 0;
    reg [19:0] timer_count = 0;

    // Crash Counter
    always @(negedge crash_clk or negedge reset) begin
        if (!reset) begin
            crash_count <= 0;
        end else begin
            crash_count <= crash_count + 1;
        end
    end

    // Time Counter
    always @(posedge clk) begin
        if (!reset) begin
            timer_count <= 0;
            ready <= 0;
            clk_count <= 0;
            reset_out <= 1;
            wait_next_reset <= 0;
        end else begin
            ready <= 1'b0;
            reset_out <= 0;
            if (clk_count < 1000) begin
                clk_count <= clk_count + 1;
            end else if (!stop) begin
                wait_next_reset <= 1;
            end else if (!wait_next_reset) begin
                timer_count <= timer_count + 1;
                clk_count <= 0;
            end else begin
                clk_count <= 0;
            end


            if (valid && !ready) begin
                ready <= 1'b1;
                rdata[19:0] <= timer_count[19:0];
                rdata[27:20] <= crash_count[7:0];
            end else if (|la_write) begin
                count <= la_write & la_input;
            end


        end
    end


endmodule
`default_nettype wire
