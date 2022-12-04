use std::fs;

fn fully_contains(x: (u32, u32), y: (u32, u32)) -> bool {
    (x.0 <= y.0 && x.1 >= y.1) || (x.0 >= y.0 && x.1 <= y.1)
}

fn overlaps(x: (u32, u32), y: (u32, u32)) -> bool {
    (x.1 >= y.0 && x.0 <= y.1) || (y.1 >= x.0 && y.0 <= x.1)
}

fn main() {
    let input = fs::read_to_string("input").unwrap();
    let ranges: Vec<((u32, u32), (u32, u32))> = input
        .lines()
        .map(|line| {
            let vec: Vec<Vec<u32>> = line
                .split(",")
                .map(|xy| xy.split("-").map(|n| n.parse::<u32>().unwrap()).collect())
                .collect();
            ((vec[0][0], vec[0][1]), (vec[1][0], vec[1][1]))
        })
        .collect();

    let answer1 = ranges.iter().fold(0, |acc, range| {
        acc + (fully_contains(range.0, range.1) as u32)
    });
    println!("Part 1: {}", answer1);

    let answer2 = ranges.iter().fold(0, |acc, range| {
        acc + (overlaps(range.0, range.1) as u32)
    });
    println!("Part 2: {}", answer2);
}
