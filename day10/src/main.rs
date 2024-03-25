enum Instruction {
    Noop,
    Addx(i64),
}

fn parse_instructions(input: &str) -> Vec<Instruction> {
    let mut v = vec![];
    for line in input.lines() {
        if line.starts_with("addx") {
            let (_, ns) = line.split_once(' ').unwrap();
            v.push(Instruction::Addx(ns.parse().unwrap()));
        } else {
            assert_eq!(line, "noop");
            v.push(Instruction::Noop);
        }
    }
    v
}

struct State<'a, I> {
    code_iter: I,
    current_instruction: Option<&'a Instruction>,
    x: i64,
    current_cycle: i64,
    is_complete: bool,
}

impl<'a, I: Iterator<Item = &'a Instruction>> State<'a, I> {
    fn new(code: I) -> Self {
        Self {
            code_iter: code,
            current_instruction: None,
            x: 1,
            current_cycle: 1,
            is_complete: false,
        }
    }

    fn tick(&mut self) {
        // If we've got an ADDX loaded in, then take it out, and finish it, leaving the next
        // fetch to the next clock cycle
        if let Some(Instruction::Addx(i)) = self.current_instruction.take() {
            self.x += i;
            self.current_cycle += 1;
            return;
        }
        self.current_instruction = self.code_iter.next();
        match self.current_instruction {
            Some(_) => {
                // if noop, this is all we need to do
                // if addx, we've stored the current instruction to be ran on the next cycle
                self.current_cycle += 1;
            }
            None => {
                self.is_complete = true;
            }
        }
    }
}

fn part1(instructions: &[Instruction]) -> i64 {
    let mut machine = State::new(instructions.iter());
    let mut strength_sum = 0;
    while !machine.is_complete {
        machine.tick();
        if (machine.current_cycle - 20) % 40 == 0 {
            strength_sum += machine.current_cycle * machine.x;
        }
    }
    strength_sum
}

fn part2(instructions: &[Instruction]) -> String {
    let mut machine = State::new(instructions.iter());
    const W: i64 = 40; // screen width
    const H: i64 = 6; // screen height

    let mut output = String::with_capacity(((W + 1) * H) as usize);
    while !machine.is_complete {
        let pixel_pos = (machine.current_cycle - 1) % 40;
        output.push(if machine.x.abs_diff(pixel_pos) <= 1 {
            '#'
        } else {
            '.'
        });
        machine.tick();
        if machine.current_cycle % 40 == 1 {
            output.push('\n');
        }
    }

    output
}

fn main() {
    let input = include_str!("../input");
    let instructions = parse_instructions(input);

    println!("Part 1: {}", part1(&instructions));

    println!("Part 2:\n{}", part2(&instructions));
}
