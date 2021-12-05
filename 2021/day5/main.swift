import Foundation

let SIZE = 1000

struct Point {
    var x = 0
    var y = 0
}

class Line: CustomStringConvertible {
    var start: Point
    var end: Point

    var description: String {
        return "Line(\(start), \(end))"
    }

    var is_horizonal: Bool {
        return start.y == end.y
    }

    var is_vertical: Bool {
        return start.x == end.x
    }

    init(start: Point, end: Point) {
        self.start = start
        self.end = end
    }
}

func readLines(input: String) -> [Line] {
    let contents = try! String(contentsOfFile: input, encoding: .utf8)
    let lines = contents.split(whereSeparator: \.isNewline)
    return lines.map { line in
        let nums = line
            .components(separatedBy: " -> ")
            .flatMap { $0.components(separatedBy: ",") }
            .map { Int($0)! }
        return Line(start: Point(x: nums[0], y: nums[1]), end: Point(x: nums[2], y: nums[3]))
    }
}

func overlapScore(lines: [Line], flag: Bool) -> Int {
    var grid = [[Int]](repeating: [Int](repeating: 0, count: SIZE), count: SIZE)
    for line in lines {
        let xs = stride(from: line.start.x, through: line.end.x, by: line.start.x < line.end.x ? 1 : -1)
        let ys = stride(from: line.start.y, through: line.end.y, by: line.start.y < line.end.y ? 1 : -1)
        switch line {
            case let l where l.is_horizonal: 
                xs.forEach { grid[line.start.y][$0] += 1 }
            case let l where l.is_vertical:
                ys.forEach { grid[$0][line.start.x] += 1 }
            default:
                if flag {
                    zip(ys, xs).forEach { grid[$0][$1] += 1 }
                }
        }
    }
    return grid
        .flatMap { $0 }
        .reduce(0) { $0 + ($1 > 1 ? 1 : 0) }
}

func main() {
    let lines = readLines(input: "./input")
    let answer1 = overlapScore(lines: lines, flag: false)
    print("Answer 1: \(answer1)")
    let answer2 = overlapScore(lines: lines, flag: true)
    print("Answer 2: \(answer2)")
}

main()