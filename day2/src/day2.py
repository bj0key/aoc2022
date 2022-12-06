with open("day2/input") as file:
    lines = file.readlines()


elf_moves = {"A": "rock", "B": "paper", "C": "scissors"}
you_moves = {"X": "rock", "Y": "paper", "Z": "scissors"}

shape_score = {"rock": 1, "paper": 2, "scissors": 3}

beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
loses = {v: k for (k, v) in beats.items()}


def win_score(you: str, elf: str) -> int:
    if you == elf:
        win_bonus = 3
    elif beats[you] == elf:
        win_bonus = 6
    else:
        win_bonus = 0
    return shape_score[you] + win_bonus


total_score = 0
for line in lines:
    elf, you = line.strip().split()
    total_score += win_score(you_moves[you], elf_moves[elf])

print(f"PART 1: {total_score}")

outcome_requirement = {"X": "lose", "Y": "draw", "Z": "win"}
total_score = 0
for line in lines:
    elf, outcome = line.strip().split()
    elf = elf_moves[elf]
    match outcome_requirement[outcome]:
        case "lose":
            you = beats[elf]
        case "draw":
            you = elf
        case "win":
            you = loses[elf]
    total_score += win_score(you, elf)

print(f"PART 2: {total_score}")
