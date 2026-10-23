module half_adder_tb;
    reg a, b;
    wire sum, carry;
    integer i;
    half_adder dut(.a(a), .b(b), .sum(sum), .carry(carry));
    initial begin
        for (i = 0; i < 4; i = i + 1) begin
            {a, b} = i;
            #10;
            if (sum !== (a ^ b) || carry !== (a & b))
                $fatal(1, "Half adder failed for a=%b b=%b", a, b);
        end
        $display("PASS: half_adder (4 cases)");
        $finish;
    end
endmodule
