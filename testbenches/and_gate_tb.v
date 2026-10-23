module and_gate_tb;
    reg a, b;
    wire y;
    integer i;
    and_gate dut(.a(a), .b(b), .y(y));
    initial begin
        for (i = 0; i < 4; i = i + 1) begin
            {a, b} = i;
            #10;
            if (y !== (a & b)) $fatal(1, "AND gate failed for a=%b b=%b", a, b);
        end
        $display("PASS: and_gate (4 cases)");
        $finish;
    end
endmodule
