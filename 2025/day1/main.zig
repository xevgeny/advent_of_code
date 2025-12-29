const std = @import("std");

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

    var pos: i32 = 50;
    var next: i32 = 0;
    var part1: i32 = 0;
    var part2: i32 = 0;

    var lines = std.mem.splitSequence(u8, text, "\n");
    while (lines.next()) |line| {
        const num: i32 = try std.fmt.parseInt(i32, line[1..], 10);
        part2 += try std.math.divTrunc(i32, num, 100);

        if (line[0] == 'L') {
            next = try std.math.mod(i32, pos - num, 100);
            if (pos != 0 and (next > pos or next == 0)) part2 += 1;
        } else {
            next = try std.math.mod(i32, pos + num, 100);
            if (next < pos) part2 += 1;
        }

        if (next == 0) part1 += 1;
        pos = next;
    }

    std.debug.print("Part1: {d}\n", .{part1});
    std.debug.print("Part2: {d}\n", .{part2});
}
