###################### Project 1 #######################
###################### Exercise 1 #######################
def caesar_decrypt(t):
    # input Caesar encrypted string, output decrypted string
    de_str = ""
    # initialize an empty string
    for char in t:
        number = ord(char) - 97
        # turn a-0 b-1 c-2....etc
        if number != -87:
            # if number = -87, the original text is \n, newline
            number = (number - 10) % 26
            # shift every number back to decode
            # the key 10 was found by another program, see attached written part
        letter = chr(number + 97)
        # turn numbers back to letters
        de_str = de_str + str(letter)
    return de_str


message = open("caesar_decrypted_113000690.txt", "w+")
# create a txt file whose name shown in the code
text = open("caesar_encrypted_113000690.txt", "r")
# open the given text file
decoded_str = caesar_decrypt(text.read())
# above 3 lines decrypted the line in the txt file
message.write(decoded_str)
# write this line into the txt file created, \n to separate lines.
message.close()
text.close()


###################### Exercise 2 #######################
def vigenere_decrypt(t):
    # input Caesar encrypted string, output decrypted string
    de_str = ""
    # initialize an empty string
    temp = 0
    # temp is used to shift back alternatively
    for char in t:
        number = ord(char) - 97
        # turn a-0 b-1 c-2....etc
        if number != -87 and number != -65:
            # if number = -87, -65 the original text is while space or newline
            temp = temp + 1
            if temp % 2 == 1:
                # if odd, it was shifted by K(+10), so -10 to shift back, even is S(-18)
                # the key 10 was found by another program, see attached written part
                number = (number - 10) % 26
            else:
                number = (number - 18) % 26
        # shift every number back to decode
        letter = chr(number + 97)
        # turn numbers back to letters
        de_str = de_str + str(letter)
    return de_str


message_v = open("vigenere_decrypted_113000690.txt", "w+")
# create a txt file whose name shown in the code
text_v = open("vigenere_encrypted_113000690.txt", "r")
# open the given text file
decoded_str = vigenere_decrypt(text_v.read())
# above 3 lines decrypted the line in the txt file
message_v.write(decoded_str)
# write this line into the txt file created, \n to separate lines.
message_v.close()
text_v.close()


###################### Exercise 3 #######################
def factor(a):
    """input a composite number n, and output its smallest prime factor. No output if n is prime.
    """
    if a % 2 == 0:
        return 2
    i = 3
    while i*i < a:
        if a % i != 0:
            i += 2
        else:
            return i


def phi_n(a):
    # input an integer that is a product of 2 primes, output phi(n), an integer
    factor_1 = factor(a)
    factor_2 = int(a / factor_1)
    # we know than n is a product of 2 primes.
    return (factor_1 - 1) * (factor_2 - 1)


def extended_ea(a, b):
    # extended euclidean algorithm, return (g, x, y) s.t. a*x + b*y = gcd(x, y)
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_ea(b % a, a)
        return g, y - (b // a) * x, x
        # recursive, applying Euclid's algorithm


def bezout_coef(a, b):
    """ input 2 integers, output the bezout coef. of b s.t. a*x + b*y = gcd(x, y)
    """
    # simply because we want y in above output, which is the 3rd element
    return extended_ea(a, b)[2]


def binary(n):
    # input an integer, output a list of 0 and 1s, the binary representation.
    if n == 0:
        # if input 0, just return empty list
        return []
    # The following just to get the list recursively
    if n % 2 == 0:
        j = n/2
        lst = binary(j)
        lst.insert(0, 0)
        return lst
    else:
        j = (n-1)/2
        lst = binary(j)
        lst.insert(0, 1)
        return lst


def fast_pow_mod(b, d, n):
    # input: base a, exponent d, modulo n
    # output: a number m = a^e mod n
    binary_lst = binary(d)
    if d == 1:
        return b % n
    if binary_lst[0] == 1:
        result = b
    if binary_lst[0] == 0:
        result = 1
    # above 2 if statement because I'd skip a to the power of 1 in the following for loop
    for i in range(1, len(binary_lst)):
        b = (b*b) % n
        # this calculates a to the power of (2^i), e.g., i = 3, calculates a^8.
        if binary_lst[i] == 1:
            # if true, the term is in the product of a^e, see details on the written part.
            result = (result*b) % n
            # multiply all terms under modulo n.
    return result


txt_r = open("rsa_encrypted_113000690.txt", 'r')
e = int(txt_r.readline()[13:])
# to extract my exponent from the txt file
n = int(txt_r.readline()[12:])
# to extract my n from the txt file
str_nums = txt_r.readline()
# this reads the 3rd line, which contains all encoded integers.
lst_nums = str_nums.split(",")
# make encoded integers to be in a list
phi_n = phi_n(n)
# to find euler phi function of n
d = bezout_coef(phi_n, e)
# d is the bezout coefficient of e by applying extended Euclidean Algorithm
decrypted_str = ""
# initialize an empty string
for num in lst_nums:
    # loop through all numbers in the list, numbers are str type.
    num = int(num)
    decoded_num = fast_pow_mod(num, d, n)
    num_str = str(decoded_num)
    # turn str type to int type, and then decode it, and then turn decoded int to str type.
    # the following just chop the each number string into 5 pieces, and present in plaintext.
    if len(num_str) == 15:
        for i in range(0, 13, 3):
            decrypted_str = decrypted_str + chr(int(num_str[i:i+3]))
    else:
        decrypted_str = decrypted_str + chr(int(num_str[0:2]))
        for i in range(2, 12, 3):
            decrypted_str = decrypted_str + chr(int(num_str[i:i + 3]))
# the following lines creates a new txt file, and writes on it.
message_r = open("rsa_decrypted_113000690.txt", "w+")
message_r.write(decrypted_str)
message_r.close()
txt_r.close()
