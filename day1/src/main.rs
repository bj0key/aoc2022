fn main() {
    let input = include_str!("../input");
    let mut elves: Vec<u32> = Vec::new();
    let mut total_sum: u32 = 0;
    for line in input.lines() {
        if line == "" {
            elves.push(total_sum);
            total_sum = 0;
        } else {
            let x = line.parse::<u32>().unwrap();
            total_sum += x;
        }
    }

    elves.sort();
    elves.reverse();

    let top = &elves[..3];
    println!("The top 3 elves are {top:?}");
    println!("Their total sum is {}", top.iter().sum::<u32>());
}
