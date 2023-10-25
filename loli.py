n = int(input())
i = 1

while i <= n:

    j = 1
    while j <= i:
        print((i - j)+1, end="")
        j += 1
        spaces = 1
    while spaces <= i:
        print(" ", end="")
        spaces += 1
        num = 1
    while num <= i:
        print(num, end="")
        num += 1
    print()

    i += 1
