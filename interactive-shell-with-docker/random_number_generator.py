from random import randint

min_number = int(input("Enter the minimum : "))
max_number = int(input("Enter the maximum : "))
if max_number < min_number:
    print("Invalid limit. Maximum should be greater than minimum. shutting down")
else:
    random_number = randint(min_number, max_number)
    print(random_number)