# Input variables supplied by main.py for each design.
yosys read_verilog $::env(DESIGN_FILE)
yosys hierarchy -check -top $::env(TOP_MODULE)
yosys synth -top $::env(TOP_MODULE)
yosys stat
