with open("day6/input") as file:
    data = file.readline()

for part, n in enumerate((4, 14), 1):
    for i in range(len(data)):
        if len(set(data[i : i + n])) == n:
            print(f"Part {part}: {i+n}")
            break
