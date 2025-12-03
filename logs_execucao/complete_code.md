# Complete Code

Here's a comprehensive code example that illustrates the concepts discussed in the theory documentation. The code includes comments to enhance readability and understanding for beginners.

```python
# Python Fundamentals - Variables and Control Flow

# 1. Introduction to Python
# Python is a versatile programming language used in web development, data science, automation, and more.

# 2. Variables in Python
# Definition: A variable is a container for storing data values.

# Declaring variables
x = 5  # Integer variable
y = 10.5  # Float variable
name = "John"  # String variable
is_active = True  # Boolean variable

# Printing the values of the variables
print("Integer:", x)
print("Float:", y)
print("String:", name)
print("Boolean:", is_active)

# Variable Naming Conventions
# Valid variable names: my_variable, variable1, _temp
# Invalid variable names: 1variable, my variable (spaces not allowed)

# 3. Data Types in Python
# Demonstrating type conversion
print("\nType Conversion:")
age = "25"  # age is a string
age_as_integer = int(age)  # Convert string to integer
print("Age as integer:", age_as_integer)

# 4. Control Flow in Python

# Conditional Statements
print("\nConditional Statements:")
if x > 5:
    print("x is greater than 5")
elif x == 5:
    print("x is equal to 5")
else:
    print("x is less than 5")

# Loops
print("\nFor Loop:")
# Using a for loop to iterate over a range of numbers
for i in range(5):
    print("Iteration:", i)

print("\nWhile Loop:")
# Using a while loop to increment x until it's less than 10
while x < 10:
    print("Current x:", x)
    x += 1  # Increment x by 1

# Break and Continue Statements
print("\nBreak and Continue Statements:")
for i in range(10):
    if i == 5:
        print("Breaking the loop at i =", i)
        break  # Exit the loop when i is 5
    print("Current i:", i)

print("\nUsing Continue Statement:")
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print("Odd number:", i)

# 5. Conclusion
# This code covered variables, data types, conditional statements, and loops.
# Feel free to ask any questions for clarification!
```

### Explanation of the Code:
1. **Variables**: The code starts by declaring different types of variables (integers, floats, strings, booleans) and printing their values.
2. **Type Conversion**: It demonstrates converting a string to an integer using the `int()` function.
3. **Conditional Statements**: The code uses `if`, `elif`, and `else` statements to evaluate the value of `x`.
4. **Loops**: It includes both `for` and `while` loops, showing how to iterate over a range and how to increment a variable.
5. **Break and Continue**: The code demonstrates how to use `break` to exit a loop and `continue` to skip certain iterations.

This example is structured to be clear and educational, making it suitable for beginners learning Python programming.
