fn parse_stacks(data: &str) -> Vec<Vec<char>> {
    let init_transformed = data
        .lines()
        .filter(|l| !l.chars().any(|c| c.is_digit(10)))
        .map(|l| Vec::from_iter(l.chars().skip(1).step_by(4)));

    let rows: Vec<Vec<char>> = Vec::from_iter(init_transformed);
    let mut stacks: Vec<Vec<char>> =
        Vec::from_iter((0..rows[0].len()).map(|_| Vec::with_capacity(64)));

    for row in rows.iter().rev() {
        for (&c, s) in row.iter().zip(&mut stacks) {
            if !c.is_whitespace() {
                s.push(c);
            }
        }
    }
    stacks
}
fn parse_moves(data: &str) -> Vec<(usize, usize, usize)> {
    let mut moves: Vec<(usize, usize, usize)> = Vec::new();
    for line in data.lines() {
        // I could use regex, but i couldn't be bothered to add a new crate to the project
        let (_, rest) = line.split_once("move ").unwrap();
        let (amount, rest) = rest.split_once(" from ").unwrap();
        let (from, to) = rest.split_once(" to ").unwrap();

        let [amount, from, to] = [amount, from, to].map(|s| s.parse::<usize>().unwrap());
        moves.push((amount, from, to));
    }
    moves
}

fn solve(data: &str) -> (String, String) {
    let (stack_data, move_data) = data.split_once("\n\n").unwrap();

    let moves = parse_moves(move_data);

    let mut stacks_pt1 = parse_stacks(stack_data);
    let mut stacks_pt2 = stacks_pt1.clone();
    let mut buffer = Vec::<char>::new();

    for m in moves {
        let (amount, from, to) = m;
        for _ in 0..amount {
            /*
            Both parts 1 and 2 are solved simultaneously, the only
            difference is how they get pushed back onto the stack
            */
            let val1 = stacks_pt1[from - 1].pop().unwrap();
            let val2 = stacks_pt2[from - 1].pop().unwrap();
            stacks_pt1[to - 1].push(val1);
            buffer.push(val2);
        }
        buffer.reverse();
        stacks_pt2[to - 1].append(&mut buffer);
    }
    let last_pt1: String = stacks_pt1.iter().map(|v| v.last().unwrap()).collect();
    let last_pt2: String = stacks_pt2.iter().map(|v| v.last().unwrap()).collect();
    (last_pt1, last_pt2)
}

fn main() {
    let data = include_str!("../input");
    let (part1, part2) = solve(&data);
    println!("Part 1: {part1}");
    println!("Part 2: {part2}");
}
