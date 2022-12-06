#![feature(is_sorted)]
fn main() {
    let input = include_str!("../input");
    let mut part1: u32 = 0;
    let mut part2: u32 = 0;
    for line in input.lines() {
        let ((l1, l2), (r1, r2)) = line
            .split_once(",")
            .map(|(x, y)| (x.split_once("-").unwrap(), y.split_once("-").unwrap()))
            .unwrap();
        let [l1, l2, r1, r2] = [l1, l2, r1, r2].map(|s| s.parse::<u32>().unwrap());
        if [l1, r1, r2, l2].is_sorted() || [r1, l1, l2, r2].is_sorted() {
            part1 += 1
        }
        if [l1, r1, l2].is_sorted() || [r1, l1, r2].is_sorted() {
            part2 += 1
        }
    }
    println!("Answer to part 1: {part1}");
    println!("Answer to part 2: {part2}");
}