with open("day1/input") as file:
    lines = file.readlines()

elves = []
total = 0
for line in lines:
    if line == "\n":
        elves.append(total)
        total = 0
    else:
        total += int(line)

elves.sort(reverse=True)
print(f"The top value is {elves[0]}, and the sum of the top three is {sum(elves[:3])}")
