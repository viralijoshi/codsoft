
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b

def exp(a,b):
     return a**b

print("performing basic calculator")
print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")
print("5.enponential")

while True:
    
    choice = (input("Enter choice(1 / 2 / 3 / 4 / 5 ): "))

    # check if choice is one of the four options
    if choice in ('1', '2', '3', '4','5'):
        try:
            num1 = int(input("Enter first number: "))
            num2 = int(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))

        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))

        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))

        elif choice == '4':
            print(num1, "/", num2, "=", divide(num1, num2))
        
        elif choice == '5':
            print(num1,"^",num2,"=",exp(num1, num2))
       
        # check if user wants to continue  calculation
        
        next = input("do you want next calculation? (yes/no): ")
        if next == "no":
          break
    else:
        print(" your input is invalid")