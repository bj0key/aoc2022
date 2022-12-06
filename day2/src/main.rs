use std::str::FromStr;

enum Strategy {
    WIN,
    LOSE,
    DRAW,
}
impl FromStr for Strategy {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "X" => Ok(Self::LOSE),
            "Y" => Ok(Self::DRAW),
            "Z" => Ok(Self::WIN),
            &_ => Err(format!("Couldn't convert {s} to a valid `Strategy`")),
        }
    }
}

#[derive(Debug, Eq, PartialEq, Clone, Copy)]
enum Move {
    ROCK,
    PAPER,
    SCISSORS,
}
impl FromStr for Move {
    type Err = String;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "X" | "A" => Ok(Move::ROCK),
            "Y" | "B" => Ok(Move::PAPER),
            "Z" | "C" => Ok(Move::SCISSORS),
            &_ => Err(format!("Couldn't convert {s} to a `Move`")),
        }
    }
}
impl Move {
    fn strategy_move(strategy: &Strategy, other: &Move) -> Move {
        match strategy {
            Strategy::DRAW => other.clone(),
            Strategy::LOSE => other.beats(),
            Strategy::WIN => other.beats().beats(),
        }
    }
    fn value(&self) -> u32 {
        match self {
            Move::ROCK => 1,
            Move::PAPER => 2,
            Move::SCISSORS => 3,
        }
    }

    fn beats(&self) -> Move {
        match self {
            Move::ROCK => Move::SCISSORS,
            Move::PAPER => Move::ROCK,
            Move::SCISSORS => Move::PAPER,
        }
    }

    fn is_beaten_by(&self, other: &Move) -> bool {
        other == &self.beats()
    }

    fn score_against(&self, other: &Move) -> u32 {
        self.value()
            + if self == other {
                3
            } else if self.is_beaten_by(other) {
                6
            } else {
                0
            }
    }
}

fn get_score(input: &str, part: u8) -> u32 {
    // PART 1: X Y Z are moves to play
    let mut score: u32 = 0;
    for line in input.lines() {
        let (elf, you) = line.split_once(" ").unwrap();
        let elf_move = Move::from_str(elf).unwrap();
        let your_move = if part == 1 {
            // PART 1: X Y Z are moves to play
            Move::from_str(you).unwrap()
        } else {
            // PART 2: X Y Z determine whether to lose, draw, or win
            Move::strategy_move(&Strategy::from_str(you).unwrap(), &elf_move)
        };
        score += your_move.score_against(&elf_move);
    }
    score
}

fn main() {
    let input = include_str!("../input");
    println!("The total score for part 1 is {}.", get_score(input, 1));
    println!("The total score for part 2 is {}.", get_score(input, 2));
}
