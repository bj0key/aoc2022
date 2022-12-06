#![feature(iter_array_chunks)]
use std::collections::HashSet;

fn char_value(c: &char) -> u32 {
    let val: u32 = c.clone() as u32;
    if c.is_lowercase() {
        val - 96
    } else {
        val - 38
    }
}

fn part_1(input: &str) -> u32 {
    let mut total = 0;
    for line in input.lines() {
        let mid = line.len() / 2;
        let mut left: HashSet<char> = HashSet::from_iter(line[..mid].chars());
        let right: HashSet<char> = HashSet::from_iter(line[mid..].chars());
        left.retain(|c| right.contains(c));

        total += char_value(&left.into_iter().next().unwrap());
    }
    total
}

fn part_2(input: &str) -> u32 {
    let mut total = 0;
    for [x, y, z] in input.lines().array_chunks() {
        let mut x: HashSet<char> = HashSet::from_iter(x.chars());
        let y: HashSet<char> = HashSet::from_iter(y.chars());
        let z: HashSet<char> = HashSet::from_iter(z.chars());
        x.retain(|c| y.contains(c));
        x.retain(|c| z.contains(c));
        total += char_value(x.iter().next().unwrap());
    }
    total
}

fn main() {
    let input = include_str!("../input");
    println!("The result for part 1 is {}", part_1(input));
    println!("The result for part 2 is {}", part_2(input));
}
