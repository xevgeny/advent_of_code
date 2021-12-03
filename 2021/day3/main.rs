const N: usize = 12;

fn most_common_bits(nums: &Vec<u32>) -> u32 {
    let mut mcb: u32 = 0;
    let mut arr: [usize; N] = [0; N];
    for num in nums.iter() {
        for i in 0..N {
            if num & (1 << i) > 0 { arr[i] += 1 }
        }
    }
    let len = nums.len();
    for i in 0..N {
        if arr[i] >= len - arr[i] { mcb |= 1 << i }
    }
    mcb
}

fn most_common_bit(nums: &Vec<u32>, pos: usize) -> bool {
    let mut n = 0;
    for num in nums.iter() {
        if num & (1 << pos) > 0 { n += 1 }
    } 
    n >= nums.len() - n
}

fn filter_nums(nums: &Vec<u32>, flag: bool) -> u32 {
    let mut vec = nums.clone();
    for i in (0..N).rev() {
        let mcb = most_common_bit(&vec, i);
        vec.retain(|x| {
            let bit = x & (1 << i) > 0;
            (bit == mcb) ^ flag
        });
        if vec.len() == 1 { break }
    }
    vec[0]
}

fn main() {
    let nums: Vec<u32> = include_str!("./input")
        .split('\n')
        .filter_map(|n| u32::from_str_radix(n, 2).ok())
        .collect();
    let mcb = most_common_bits(&nums);
    println!("power consumption: {}", mcb * (!mcb & 0xfff));
    println!("life support rating: {}", filter_nums(&nums, true) * filter_nums(&nums, false));
}