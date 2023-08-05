import math

conv_fac = 0.621371


def add(number1, number2):
    """
    This function helps you add numbers and print it you would need to put the numbers inside the function name added
    to the code that should look something like this. add(1, 2). If its an input it doesnt need to converted to
    a string.
    :param number1: The first number
    :param number2: The second number
    :return:
    """
    if type(number1) == str:
        try:
            number1 = int(number1)
        except:
            return f"[EXCEPTION][{number1} is not a number]"
    if type(number2) == str:
        try:
            number2 = int(number2)
        except:
            return f"[EXCEPTION][{number2} is not a number]"
    print(number1 + number2)
    print(f"The sum of {number1} and {number2} is {number1 + number2}")
    return number1 + number2


def float_add(number1, number2):
    """
    This function helps you add numbers and print it you would need to put the numbers inside the function name added
    to the code that should look something like this. add(1.5, 2.3). If its an input it doesnt need to converted to
    a string.
    :param number1: The first number
    :param number2: The second number
    :return:
    """
    if type(number1) == str:
        try:
            number1 = float(number1)
        except:
            return f"[EXCEPTION][{number1} is not a number]"
    if type(number2) == str:
        try:
            number2 = float(number2)
        except:
            return f"[EXCEPTION][{number2} is not a number]"
    print(number1 + number2)
    print(f"The sum of {number1} and {number2} is {number1 + number2}")
    return number1 + number2


def sqrt(number):
    """
    This returns and prints the square root of the number
    :param number: Number
    :return:
    """
    if type(number) == str:
        try:
            number1 = float(number)
        except:
            return f"[EXCEPTION][{number} is not a number]"
    sqrtnumber = math.sqrt(number)
    print(sqrtnumber)
    print(f"Square root of {number} is {sqrtnumber}")
    return sqrtnumber


def areaTriangle(a, b, c):
    """
    Gives area of a triangle using Heron's formula
    :param a: length of Side A
    :param b: length of Side B
    :param c: length of Side C
    :return:
    """
    if type(a) == str:
        try:
            a = float(a)
        except:
            return f"{a} is not a number"
    if type(b) == str:
        try:
            b = float(b)
        except:
            return f"{b} is not a number"
    if type(c) == str:
        try:
            c = float(c)
        except:
            return f"{c} is not a number"
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    print(f'The area of the triangle is {area}')


def kmtomile(kilometer):
    """
    Converts Kilometer to mile using the conversion factor.
    :param kilometer:
    :return:
    """
    if type(kilometer) == str:
        try:
            kilometers = float(kilometer)
        except:
            return f"{kilometer} is not a number"
    miles = kilometers * conv_fac
    print('%0.2f kilometers is equal to %0.2f miles' % (kilometers, miles))
    return miles


def celciustofaren(celsius):
    """
    Converts Celsius to Fahrenheit
    :param celsius:
    :return:
    """
    fahrenheit = (celsius * 1.8) + 32
    print('%0.1f degree Celsius is equal to %0.1f degree Fahrenheit' % (celsius, fahrenheit))
    return fahrenheit


def volume_box(l, b, h):
    """
    Finds volume of a box
    :param l: Length
    :param b: Breadth
    :param h: Height
    :return:
    """
    if type(l) == str:
        try:
            l = int(l)
        except:
            return f"[EXCEPTION][{l} is not a number]"
    if type(b) == str:
        try:
            b = int(b)
        except:
            return f"[EXCEPTION][{b} is not a number]"
    if type(h) == str:
        try:
            h = int(h)
        except:
            return f"[EXCEPTION][{h} is not a number]"
    volume = l * b * h
    print(f"Volume of the box is {volume}³")
    return volume


def adult(age):
    """
    Prints if person is adult or not. Age for adult taken as 18
    :param age: Age
    :return:
    """
    if type(age) == str:
        try:
            age = int(age)
        except:
            return f"[EXCEPTION][{age} is not a number]"
    if age > 18:
        print("You are Adult")
    else:
        print("You are not Adult")
    return
