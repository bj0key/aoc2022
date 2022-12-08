with open("day7/input") as file:
    lines = file.readlines()


directory_sizes: dict[str, int] = {}
line_iter = iter(lines)


def total_directory_size(directory: str):
    total_size = 0
    for line in line_iter:
        if line.startswith("$ cd .."):
            # end of directory
            break
        elif line.startswith("$ cd"):
            # start of a new directory
            dir_name = line.rsplit("cd", 1)[-1]
            total_size += total_directory_size(directory + "/" + dir_name)
        elif line.startswith("$ ls") or line.startswith("dir"):
            # these lines can be completely ignored
            continue
        else:
            # line is a file and its filesize
            file_size = int(line.split(" ", 1)[0])
            total_size += file_size

    directory_sizes[directory] = total_size
    return total_size


total_directory_size("/")


part1 = sum(size for size in directory_sizes.values() if size <= 100_000)
print(f"Part 1: {part1}")

root_size = directory_sizes["/"]
# 70M in capacity, 30M should be free, so we can have 40M still used and be fine
space_to_free = root_size - 40_000_000
part2 = min(d for d in directory_sizes.values() if d >= space_to_free)
print(f"Part 2: {part2}")
input()
