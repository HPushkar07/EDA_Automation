"""Beginner-friendly EDA flow: compile, simulate, synthesize, and report."""
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
DESIGNS = ("and_gate", "or_gate", "half_adder")


def parse_log(log_text):
    """Return tool messages labelled ERROR or WARNING, ignoring case."""
    errors = []
    warnings = []
    for line in log_text.splitlines():
        if re.search(r"\b(?:ERROR|FATAL)\s*:", line, re.IGNORECASE):
            errors.append(line.strip())
        elif re.search(r"\bWARNING\s*:", line, re.IGNORECASE):
            warnings.append(line.strip())
    return errors, warnings


def execute(command, *, env=None):
    """Run a tool safely, collecting output and exit status."""
    try:
        result = subprocess.run(
            command, cwd=ROOT, env=env, capture_output=True, text=True,
            timeout=120, check=False
        )
        return result.returncode, result.stdout + result.stderr
    except FileNotFoundError:
        return 127, f"ERROR: Tool not found: {command[0]}\n"
    except subprocess.TimeoutExpired:
        return 124, f"ERROR: Tool timed out: {command[0]}\n"


def run_design(name):
    design = ROOT / "designs" / f"{name}.v"
    testbench = ROOT / "testbenches" / f"{name}_tb.v"
    executable = BUILD / f"{name}.vvp"
    messages = []
    stages = {"compile": "SKIP", "simulation": "SKIP", "synthesis": "SKIP"}

    code, output = execute([
        "iverilog", "-g2012", "-s", f"{name}_tb", "-o", str(executable),
        str(design), str(testbench)
    ])
    messages.append(output)
    stages["compile"] = "PASS" if code == 0 else "FAIL"

    if code == 0:
        code, output = execute(["vvp", str(executable)])
        messages.append(output)
        stages["simulation"] = "PASS" if code == 0 and f"PASS: {name}" in output else "FAIL"

    if stages["simulation"] == "PASS":
        env = os.environ.copy()
        env["DESIGN_FILE"] = str(design)
        env["TOP_MODULE"] = name
        code, output = execute(["yosys", "-c", str(ROOT / "synth.tcl")], env=env)
        messages.append(output)
        stages["synthesis"] = "PASS" if code == 0 else "FAIL"

    log = "\n".join(messages)
    (BUILD / f"{name}.log").write_text(log, encoding="utf-8")
    errors, warnings = parse_log(log)
    passed = all(stage == "PASS" for stage in stages.values())
    return {"name": name, "stages": stages, "errors": errors,
            "warnings": warnings, "passed": passed}


def save_report(results):
    lines = ["EDA FLOW AUTOMATION REPORT",
             f"Generated: {datetime.now().isoformat(timespec='seconds')}", ""]
    for result in results:
        stages = result["stages"]
        lines.append(f"{result['name']}: {'PASS' if result['passed'] else 'FAIL'}")
        lines.append("  Compile: {compile} | Simulation: {simulation} | Synthesis: {synthesis}".format(**stages))
        lines.append(f"  Errors: {len(result['errors'])} | Warnings: {len(result['warnings'])}")
        for message in result["errors"] + result["warnings"]:
            lines.append(f"    {message}")
        lines.append("")
    passed = sum(result["passed"] for result in results)
    lines.append(f"TOTAL: {passed}/{len(results)} designs passed")
    report = "\n".join(lines) + "\n"
    (BUILD / "report.txt").write_text(report, encoding="utf-8")
    return report


def main():
    BUILD.mkdir(exist_ok=True)
    print("===== EDA AUTOMATION TOOL =====")
    results = []
    for name in DESIGNS:
        print(f"\nRunning {name}...")
        result = run_design(name)
        results.append(result)
        print(f"  Compile: {result['stages']['compile']}")
        print(f"  Simulation: {result['stages']['simulation']}")
        print(f"  Synthesis: {result['stages']['synthesis']}")
        print(f"  Result: {'PASS' if result['passed'] else 'FAIL'}")
    print("\n" + save_report(results))
    print("Report saved to build/report.txt")
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
