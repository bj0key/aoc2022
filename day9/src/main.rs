#![feature(get_many_mut)]
use std::collections::HashSet;

#[derive(PartialEq, Eq, Debug)]
enum Direction {
    UP,
    DOWN,
    RIGHT,
    LEFT,
}
impl Direction {
    fn from_str(dir: &str) -> Option<Direction> {
        match dir {
            "U" => Some(Direction::UP),
            "D" => Some(Direction::DOWN),
            "L" => Some(Direction::LEFT),
            "R" => Some(Direction::RIGHT),
            _ => None,
        }
    }
}
#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Pos(i32, i32);
#[derive(Clone)]
struct Knot {
    x: i32,
    y: i32,
    visited: HashSet<(i32, i32)>,
}
impl Knot {
    fn new() -> Knot {
        let mut k = Knot {
            x: 0,
            y: 0,
            visited: HashSet::new(),
        };
        k.visited.insert((k.x, k.y));
        k
    }

    fn move_in_direction(&mut self, direction: &Direction) {
        match direction {
            Direction::RIGHT => self.x += 1,
            Direction::LEFT => self.x -= 1,
            Direction::UP => self.y += 1,
            Direction::DOWN => self.y -= 1,
        }
        self.visited.insert((self.x, self.y));
    }
    fn distance_towards(&self, target: &Knot) -> i32 {
        let dx = (self.x - target.x).abs();
        let dy = (self.y - target.y).abs();
        dx.max(dy)
    }
    fn move_towards(&mut self, target: &Knot) {
        while self.distance_towards(target) > 1 {
            let dx = (target.x - self.x).clamp(-1, 1);
            let dy = (target.y - self.y).clamp(-1, 1);
            self.x += dx;
            self.y += dy;
            self.visited.insert((self.x, self.y));
        }
    }
}

fn main() {
    let input = include_str!("../input");

    let mut rope: Vec<Knot> = Vec::with_capacity(10);
    for _ in 0..10 {
        rope.push(Knot::new());
    }

    for (c, i) in input.lines().map(|l| {
        let (x, y) = l.split_once(" ").unwrap();
        (x, y.parse::<u32>().unwrap() as u32)
    }) {
        let dir = Direction::from_str(c).unwrap();
        for _ in 0..i {
            rope[0].move_in_direction(&dir);
            for i in 1..10 {
                if let Ok([x, y]) = rope.get_many_mut([i - 1, i]) {
                    y.move_towards(x);
                }
            }
        }
    }

    println!("Part 1: {}", &rope[1].visited.len());
    println!("Part 2: {}", &rope[9].visited.len());
}
