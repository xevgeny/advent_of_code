const std = @import("std");

inline fn isInvalid1(num: []u8) bool {
    if (num.len % 2 != 0) return false;
    return std.mem.eql(u8, num[0 .. num.len / 2], num[num.len / 2 .. num.len]);
}

inline fn isInvalid2(num: []u8) bool {
    var seq_len: usize = 1;
    while (seq_len <= num.len / 2) : (seq_len += 1) {
        if (num.len % seq_len != 0) continue;
        var i: usize = seq_len;
        const seq = num[0..seq_len];
        var invalid = true;
        while (i < num.len) : (i += seq_len) {
            invalid &= std.mem.eql(u8, seq, num[i .. i + seq_len]);
            if (!invalid) break;
        }
        if (invalid) return true;
    }
    return false;
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    if (args.len != 2) return error.MissingArgument;

    const file = try std.fs.cwd().openFile(args[1], .{});
    defer file.close();

    const text = try file.readToEndAlloc(allocator, 1024 * 1024);
    defer allocator.free(text);

    var part1: u64 = 0;
    var part2: u64 = 0;

    var buf: [32]u8 = undefined;
    var lines = std.mem.splitScalar(u8, text, ',');
    while (lines.next()) |line| {
        var parts = std.mem.splitScalar(u8, line, '-');
        const s0 = parts.next().?;
        const s1 = parts.next().?;
        const min = try std.fmt.parseInt(u64, s0, 10);
        const max = try std.fmt.parseInt(u64, s1, 10);

        var i = min;
        while (i <= max) : (i += 1) {
            const num_len = std.fmt.printInt(&buf, i, 10, .lower, .{});
            const num = buf[0..num_len];
            if (isInvalid1(num)) part1 += i;
            if (isInvalid2(num)) part2 += i;
        }
    }

    std.debug.print("Part 1: {d}\n", .{part1});
    std.debug.print("Part 2: {d}\n", .{part2});
}
