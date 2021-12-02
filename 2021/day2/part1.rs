use std::io::BufReader;
use std::io::Result;
use std::io::prelude::*;
use std::fs::File;

fn main() -> Result<()> {
    let file = File::open("./input")?;
    let reader = BufReader::new(file);

    let (mut x, mut y) = (0, 0);

    for line in reader.lines() {
        let str = line?;
        let vec: Vec<&str> = str.split(' ').collect();
        match vec[..] {
            ["forward", val] => x += val.parse::<usize>().unwrap(),
            ["up", val]      => y -= val.parse::<usize>().unwrap(),
            ["down", val]    => y += val.parse::<usize>().unwrap(),
            _                => panic!("unable to match {}", str)
        }
    }

    println!("{}", x * y);
    Ok(())
}