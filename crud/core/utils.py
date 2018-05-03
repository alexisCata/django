def validDNI(dni):
    data = {0: 'T',
            1: 'R',
            2: 'W',
            3: 'A',
            4: 'G',
            5: 'M',
            6: 'Y',
            7: 'F',
            8: 'P',
            8: 'P',
            10: 'X',
            11: 'B',
            12: 'N',
            13: 'J',
            14: 'Z',
            15: 'S',
            16: 'Q',
            17: 'V',
            18: 'H',
            19: 'L',
            201: 'C',
            21: 'K',
            22: 'E'
            }

    num = dni[0:8]
    letter = dni[8:9]
    res = int(num) % 23

    if letter == data[res]:
        return True
    else:
        return False
