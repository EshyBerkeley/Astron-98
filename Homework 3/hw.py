
import math

def comp_pow(x, y):
    res = x
    for i in range(0, y - 1):
        res *= x
    return res

def find_min_max(temps):
    min_temp = temps[0]
    max_temp = temps[0]
    for temp in temps:
        if temp < min_temp:
            min_temp = temp
        if temp > max_temp:
            max_temp = temp
    return min_temp, max_temp

def is_weekend(day):
    return day == 6 or day == 7

def comp_fuel_efficiency(miles, gallons):
    return miles / gallons

def encode_data(data):
    res = data
    num_digits = int(math.log10(data)) + 1
    last_digit = data % 10
    res //= 10
    res += last_digit * pow(10, num_digits - 1)
    return res, num_digits, last_digit

def for_min(nums):
    min_num = nums[0]
    for num in nums:
        if num < min_num:
            min_num = num
    return min_num

def for_max(nums):
    max_num = nums[0]
    for num in nums:
        if num > max_num:
            max_num = num
    return max_num

def while_min(nums):
    min_num = nums[0]
    i = 1
    while i < len(nums):
        if nums[i] < min_num:
            min_num = nums[i]
        i += 1
    return min_num

def while_max(nums):
    max_num = nums[0]
    i = 1
    while i < len(nums):
        if nums[i] > max_num:
            max_num = nums[i]
        i += 1
    return max_num

def find_num_vowels_consonants(s):
    vowels = ['a', 'e', 'i', 'o', 'u']
    num_vowels = 0
    num_consonants = 0
    for char in s:
        if char in vowels:
            num_vowels += 1
        elif char.isalpha():
            num_consonants += 1
    return num_consonants, num_vowels

def comp_root(num):
    sum = 0
    num_digits = int(math.log10(num)) + 1
    for i in range(0, num_digits):
        last_digit = num % 10
        num //= 10
        sum += last_digit
    return sum