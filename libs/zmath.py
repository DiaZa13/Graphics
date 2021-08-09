# Librería de operaciones matemáticas

def subtract(v1, v2):
    result = []

    if len(v1) == len(v2):
        for i in range(len(v1)):
            result.append(v1[i] - v2[i])
    else:
        return

    return result

def cross(a, b):
    result = []

    if len(a) == 2 and len(b) == 2:
        result.append((a[0] * b[1]) - (a[1] * b[0]))
        return result[0]
    else:
        result.append((a[1] * b[2]) - (a[2] * b[1]))
        result.append((a[2] * b[0]) - (a[0] * b[2]))
        result.append((a[0] * b[1]) - (a[1] * b[0]))

    return result

def dot(a, b):
    result = []
    dot_result = 0

    if len(a) == len(b):
        for i in range(len(a)):
            result.append(a[i] * b[i])
        for r in result:
            dot_result += r
    else:
        return

    return dot_result

def normalize(v):
    result = []
    r = 0
    for a in v:
        r += pow(a, 2)

    r = pow(r, 0.5)

    if r != 0:
        for a in v:
            result.append(a / r)
    else:
        return v

    return result
