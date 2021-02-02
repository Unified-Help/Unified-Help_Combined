diction = {"January": [121, 123, 125, 125]}
for key, value in diction.items():
    temp = [key]
    for i in value:
        temp.append(i)
print(temp)
