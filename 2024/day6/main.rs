use fxhash::FxHashSet;
use std::fs;

#[derive(Clone, Copy, Hash, Eq, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    fn next(&self, dir: i32, xs: &Vec<Vec<char>>) -> Option<Self> {
        let (x, y) = (self.x + DIRS[dir as usize].0, self.y + DIRS[dir as usize].1);
        if x >= 0 && x < xs.len() as i32 && y >= 0 && y < xs[0].len() as i32 {
            Some(Point{x, y})
        } else {
            None
        }
    }
}

const DIRS: [(i32, i32); 4] = [(-1, 0), (0, 1), (1, 0), (0, -1)];

fn count_visited(xs: &Vec<Vec<char>>, start_pos: (Point, i32)) -> usize {
    let mut visited = FxHashSet::default();
    let (mut pos, mut dir) = start_pos;
    loop {
        visited.insert((pos.x, pos.y));
        if let Some(next_pos) = pos.next(dir, xs) {
            if xs[next_pos.x as usize][next_pos.y as usize] == '#' {
                dir = (dir + 1) % 4;
            } else {
                pos = next_pos;
            }
        } else {
            break;
        }
    }
    visited.len()
}

fn detect_loop(
    xs: &Vec<Vec<char>>,
    start_pos: (Point, i32),
    prev: &FxHashSet<(i32, i32, i32)>,
    obstacle_pos: Point,
) -> bool {
    let mut visited = prev.clone();
    let (mut pos, mut dir) = start_pos;
    loop {
        let curr = (pos.x, pos.y, dir);
        if visited.contains(&curr) {
            return true;
        }
        visited.insert(curr);
        if let Some(next_pos) = pos.next(dir, xs) {
            if xs[next_pos.x as usize][next_pos.y as usize] == '#' || next_pos == obstacle_pos {
                dir = (dir + 1) % 4;
            } else {
                pos = next_pos;
            }
        } else {
            break;
        }
    }
    false
}

fn cont_unique_pos(xs: &Vec<Vec<char>>, start_pos: (Point, i32)) -> usize {
    let mut path = FxHashSet::default();
    let mut visited = FxHashSet::default();
    let (mut pos, mut dir) = start_pos;
    let mut res = 0;
    loop {
        let curr = (pos.x, pos.y, dir);
        path.insert((pos.x, pos.y));
        if let Some(next_pos) = pos.next(dir, xs) {
            if xs[next_pos.x as usize][next_pos.y as usize] == '#' {
                dir = (dir + 1) % 4;
            } else {
                if !path.contains(&(next_pos.x, next_pos.y)) && detect_loop(xs, (pos, dir), &visited, next_pos)
                {
                    res += 1;
                }
                pos = next_pos;
            }
            visited.insert(curr);
        } else {
            break;
        }
    }
    res
}

fn main() {
    let input = fs::read_to_string("input").unwrap();
    let xs: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    let start_pos: (Point, i32) = xs
        .iter()
        .enumerate()
        .find_map(|(i, line)| {
            line.iter()
                .position(|&c| c == '^')
                .map(|j| (Point::new(i as i32, j as i32), 0))
        })
        .unwrap_or((Point::new(0, 0), 0));

    println!("Part 1: {:?}", count_visited(&xs, start_pos));
    println!("Part 2: {:?}", cont_unique_pos(&xs, start_pos));
}
