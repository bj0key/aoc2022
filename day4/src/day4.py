with open("day4/input") as file:
    lines = file.readlines()

full_overlaps = 0
any_overlaps = 0
for line in lines:
    (x1, y1), (x2, y2) = (map(int, h.split("-")) for h in line.split(","))
    full_overlaps += x1 <= x2 <= y2 <= y1 or x2 <= x1 <= y1 <= y2
    any_overlaps += x1 <= x2 <= y1 or x2 <= x1 <= y2




print(full_overlaps)
print(any_overlaps)

# Here's a fun one-liner for ya!
# print(*map(sum,zip(*((a<=c<=d<=b or c<=a<=b<=d,a<=c<=b or c<=a<=d)for(a,b),(c,d)in((map(int,h.split("-"))for h in line.split(","))for line in lines)))))
