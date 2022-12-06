with open("day6/input") as file:
    data = file.readline()

for i in range(len(data)):
    if len(set(data[i:i+4])) == 4:
        print(i+4)
        break

for i in range(len(data)):
    if len(set(data[i:i+14])) == 14:
        print(i+14)
        break
