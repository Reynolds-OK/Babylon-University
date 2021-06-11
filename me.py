# Write a program that reads an integer from the user. Then your program should
# display a message indicating whether the integer is even or odd.
integer = int(input('Enter Integer: '))
if integer% 2 == 0:
    print('It is even')
else:
    print('It is odd')


# 2. A string is a palindrome if it is identical forward and backward. For example
# “anna”, “civic”, “level”and“hannah”are all examples of palindromic words.Write a
# program that reads a string from the user and uses a loop to determines whether or
# not it is a palindrome.
word = input('Word: ')


if word == word[::-1]:
    print('It is a palindrome')
else:
    print('It is not a palindrome')


# 3. Write a program that reads integers from the user and stores them in a list.
# Yourprogram should continue reading values until the user enters 0. Then it
# should display all of the values entered by the user(except for the 0) in order from
# smallest to largest, with one value appearing on each line.
numbers = []
while True:
    number = int(input('Enter a number: '))
    if number == 0:
        break
    numbers.append(number)

numbers.sort()

for each in numbers:
    print(each)


# 4. Two words are anagrams if they contain all of the same letters, but in a
# differentorder. For example, “evil” and “live” are anagrams because each contains
# one ‘e’, one ‘i’, one ‘l’, and one ‘v’. Create a program that reads two strings from
# the user, determines whether or not they are anagrams.
first = input('Enter first letter: ')
second = input('Enter second letter: ')

for letter in first:
    if letter not in second and first.count(letter) != second.count(letter):
        print('It is not an anagram')
        break
else:
    print('It is an anagram')
    

# 5. Write a function that takes three numbers as parameters, and returns the median
# value of those parameters as its result
numbers = []


def median(first, second, third):
    numbers.append(first)
    numbers.append(second)
    numbers.append(third)
    numbers.sort()
    index = int((len(numbers)+1)/2)
    return numbers[index-1]


print(median(4, 5, 2))
