# EDA Flow Automation Tool

A beginner-friendly Python automation project that compiles, simulates, and synthesizes three Verilog designs (AND gate, OR gate, and half adder), then generates a pass/fail report.

## Requirements (Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip iverilog yosys
python3 -m pip install pytest
```

Use a Python virtual environment for Pytest if your distribution restricts system-wide pip installs.

## Run

```bash
chmod +x run.sh
./run.sh
```

Or run `python3 main.py` directly.

Output files are created in `build/`:
- `report.txt`: summary of the results
- `and_gate.log`, `or_gate.log`, `half_adder.log`: tool outputs
- `*.vvp`: compiled simulation programs

If the tools are missing, the runner reports failure instead of claiming success.

## Run unit tests

```bash
python3 -m pytest -q
```

The tests verify the Python log parser, and do not require Verilog tools.

## Project flow

1. `main.py` compiles each design and its testbench with `iverilog`.
2. `vvp` executes the testbench. Assertions (`$fatal`) cause failures to return nonzero status.
3. Yosys executes `synth.tcl`, reading the design and generating synthesis statistics.
4. Python extracts errors and warnings, writes individual logs, and creates `build/report.txt`.

This project runs designs **sequentially**. It does not include parallel regression execution or a measured performance improvement.
