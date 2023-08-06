import string

def write(filename, dictionary):
    alphabet = dict(enumerate(string.printable))
    alphabet = {value : key for (key, value) in alphabet.items()}

    array = []

    for i in dictionary:
        if isinstance(i, bool):
            if i == True:
                array.append(103)

            else:
                array.append(104)

        elif isinstance(i, int):
            array.append(102)
            array.append(i)

        else:
            for k in i:
                array.append(alphabet[k])

        array.append(100)

        if isinstance(dictionary[i], bool):
            if dictionary[i] == True:
                array.append(103)

            else:
                array.append(104)

        elif isinstance(dictionary[i], int):
            array.append(102)
            array.append(dictionary[i])

        else:
            for k in dictionary[i]:
                array.append(alphabet[k])

        array.append(101)

    with open(filename, "wb") as file:
        file.write(bytearray(array))

def read(filename):
    alphabet = dict(enumerate(string.printable))

    with open(filename, "rb") as file:
        array = file.read()

    result = {}
    int_state = False
    str = ""
    left = ""

    for i in array:
        if int_state:
            str = i
            int_state = False

        elif i == 100:
            left = str
            str = ""

        elif i == 101:
            result[left] = str
            str = ""

        elif i == 102:
            int_state = True

        elif i == 103:
            str = True

        elif i == 104:
            str = False
        
        else:
            str += alphabet[i]

    return result