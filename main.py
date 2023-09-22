import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import string

letters = string.ascii_lowercase
random_string = ''.join(random.choice(letters) for i in range(7))

#print(random_string)

# Ask for file name
filename = input("Enter file name: ")

# Define roulette sequence
roulette_sequence = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
                     31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]  # np.arange(0, 37)

# Ask for current roulette number
def enter_number():
    while True:
        current_roulette = int(input("Enter current roulette number: "))
        if not(current_roulette>=0 and current_roulette<=36):
            print('Invalid values. Acceptable values 0,1,2,3,..., 34,35,36')
        else:
            break
    return current_roulette

previous_roulette = enter_number()

# Initialize arrays
difference = []
direction = []
bounce = []
bnc='n'
# Loop to ask for input
while True:
    # Ask for direction, roulette number and bounce
    print('======================== New Round? ======================')
    while True:
        dir = input("Enter direction or exit (l/r/exit): ")
        if dir != 'l' and dir!= 'r' and dir!='exit':
            print('Invalid values. Acceptable values are l,r,exit.')
        else:
            break
    if dir == "exit":
        break
    num = enter_number()
    #bnc = input("Did the ball bounce? (y/n): ")

    # Print entered values and ask for confirmation
    print(f"Direction: {dir}, Number: {num}, Bounced: {bnc}")
    confirm = input("Press any key if this is correct. If there was an error press z ")

    if confirm == "z":
        print('Error noted, you can try again.')
        continue

    # Append values to arrays
    direction.append(dir)
    bounce.append(bnc)

    # Calculate slot difference and append to difference array
    p1 = roulette_sequence.index(previous_roulette)
    p2 = roulette_sequence.index(num)
    slot_diff = p2 - p1
    if slot_diff < 0:
        slot_diff = slot_diff + 37
    print(f"Position difference: {slot_diff}")
    difference.append(slot_diff)
    previous_roulette = num

# Convert bounce array to boolean
bounce = np.array(bounce) == "y"


df = pd.DataFrame({'difference': difference, 'bounce': bounce, 'direction': direction})
df.to_csv(f'{filename}_{random_string}.csv')
# Group by the categories and calculate the statistics
categories = [('True', 'l'), ('True', 'r'), ('False', 'r'), ('False', 'l')]
for b, d in categories:
    group = df[(df['bounce'] == (b == 'True')) & (df['direction'] == d)]
    if not group.empty:
        avg = group['difference'].mean()
        std = group['difference'].std()
        group.hist(column='difference', bins=np.arange(-1,37)+0.5, ec="k")
        print(group)
        print(f"Category ({b}, {d}): Avg={avg:.2f}, Std={std:.2f}")
        plt.show()
