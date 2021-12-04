use std::str::FromStr;
use std::fmt;

struct Square {
    number: u32,
    marked: bool,
}

impl fmt::Debug for Square {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.marked { write!(f, "{}*", self.number) }
        else { write!(f, "{}", self.number) }
    }
}

#[derive(Debug)]
struct Board {
    board: Vec<Vec<Square>>,
    bingo: bool
}

impl Board {
    fn mark(&mut self, number: u32) {
        'outer: for row in self.board.iter_mut() {
            for square in row.iter_mut() {
                if square.number == number {
                    square.marked = true;
                    break 'outer
                }
            }
        }

        let winning_row = self.board.iter().fold(false, |y, row| {
            y | row.iter().fold(true, |x, square| x & square.marked)
        });
        let winning_col = (0..self.board[0].len()).fold(false, |x, col| {
            x | self.board.iter().fold(true, |y, row| y & row[col].marked)
        });
        self.bingo = winning_row | winning_col
    }

    fn score(&self, draw: u32) -> u32 {
        let sum_unmarked = self.board.iter().fold(0u32, |y, row| {
            y + row.iter().fold(0u32, |x, square| {
                if !square.marked { x + square.number } else { x }
            })
        });
        draw * sum_unmarked
    }
}

fn read_draw_nums(s: &str) -> Vec<u32> {
    s.split(',').filter_map(|n| u32::from_str(n).ok()).collect()
}

fn read_boards(boards: &[&str]) -> Vec<Board> {
    boards.iter().map(|s| {
        let board: Vec<Vec<Square>> = s.split('\n')
            .filter_map(|row_str| {
                let row: Vec<Square> = row_str.split(' ')
                    .filter_map(|n| u32::from_str(n).ok())
                    .map(|n| Square { number: n, marked: false })
                    .collect();
                if row.len() > 0 { Some(row) } else { None }
            })
            .collect();
        Board { board: board, bingo: false }
    })
    .collect()
}

fn main() {
    let input: Vec<&str> = include_str!("input").split("\n\n").collect();
    let draw_nums = read_draw_nums(input[0]);
    let mut boards = read_boards(&input[1..]);
    let (total_boards, mut total_winners) = (boards.len(), 0);

    for draw in draw_nums.into_iter() {
        for board in boards.iter_mut() {
            if board.bingo { continue }
            board.mark(draw);
            if board.bingo {
                total_winners += 1;
                if total_winners == 1 {
                    println!("Board {:?} wins first, score {}", board.board, board.score(draw))
                }
                if total_winners == total_boards {
                    println!("Board {:?} wins last, score {}", board.board, board.score(draw));
                    return
                }
            }
        }
    }
}
