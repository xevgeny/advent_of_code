use std::fs;

// Lowercase item types a through z have priorities 1 through 26.
// Uppercase item types A through Z have priorities 27 through 52.
fn score(c: char) -> u32 {
    match c {
        'a'..='z' => c as u32 - 'a' as u32 + 1,
        'A'..='Z' => c as u32 - 'A' as u32 + 27,
        _ => panic!("Invalid char: {}", c),
    }
}

fn find_duplicate(s: &str) -> u32 {
    let (left, right) = s.split_at(s.len() / 2);
    for c in left.chars() {
        if right.contains(c) {
            return score(c);
        }
    }
    return 0;
}

fn find_duplicate3(s1: &str, s2: &str, s3: &str) -> u32 {
    for c in s1.chars() {
        if s2.contains(c) && s3.contains(c) {
            return score(c);
        }
    }
    return 0;
}

fn main() {
    let input = fs::read_to_string("input").unwrap();
    let lines: Vec<&str> = input.lines().collect();
    let part1: u32 = lines.iter().map(|s| find_duplicate(s)).sum();
    println!("Part 1: {}", part1);
    let part2: u32 = lines
        .chunks(3)
        .map(|c| find_duplicate3(c[0], c[1], c[2]))
        .sum();
    println!("Part 2: {}", part2);
}
