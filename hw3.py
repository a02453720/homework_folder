# # #Question 3.4
# # for i in range(2):
# #     for i in range(8):
# #         print('@', end="")
# #     print()


# # #Question 3.9
# # number = input("enter a 7 to 10 digit number: ")
# # length = len(number)
# # as_int = int(number)
# # for i in range(length):
# #     print((as_int//(10**(length-i-1))%10))




# #question 3.11

# #For this question I used some weird formatting of the while loop so that the program output could look exactly like the question example

# gallons = 0
# trip_mpg = []
# #Checking first iteration (It has to be ordered this way for the program to quit right when the user enters -1)
# gallons = float(input("Enter gallons used (-1 to end): "))
# if gallons == -1:
#     exit(0) #I know we haven't covered this but I know some python already and I'm trying to cover all possible user entry scenarios
# miles = float(input("Enter miles driven: "))
# mpg = miles/gallons
# print("The miles per gallon for this tank was", mpg)
# trip_mpg.append(mpg)
# gallons = float(input("Enter gallons used(-1 to end): "))
# while gallons != -1:
    
#     miles = float(input("Enter miles driven: "))
#     mpg = miles/gallons
#     print("The miles per gallon for this tank was", mpg)
#     trip_mpg.append(mpg)
#     gallons = float(input("Enter gallons used(-1 to end): "))

# total_mpg = 0
# for a in trip_mpg:
#     total_mpg += a
# total_mpg /= len(trip_mpg)
# print("You're overall miles per gallon was", total_mpg)

#3.12
# num = str(input("input an integer: "))
# length = len(num)
# for i in range(length//2 + 1):
#     #reading string backwards and comparing it with reading forwards
#     if num[i] != num[-i-1]:
#         print("Not a palindrome")
#         break

# if i+1 == (length//2) + 1:
#     print("Palindrome!!!")


#3.14
pi = 4
roundpi = 0
counter = 0
addsubtract = 0
num = 3
approximation_requirements = []
approx1 = False
approx2 = False
for i in range(3000):
    previous = pi
    if addsubtract%2 == 0:
        pi -= 4/num
    else:
        pi += 4/num
    addsubtract += 1
    num +=2
    counter +=1
    print("Series:", counter, "Pi:", pi)
    if previous > 3.14 and previous <3.15 and pi >3.14 and pi <3.15 and not approx1:
        approximation_requirements.append(counter)
        approx1 = True
    if previous > 3.141 and previous <3.142 and pi >3.141 and pi <3.142 and not approx2:
        approximation_requirements.append(counter)
        approx2 = True
    
print("iterations required for each level of approximation",approximation_requirements)

