

def itobin(x: int) -> str:
    return format(x, '04b')


def hextobin(hexstr: str) -> str:
    binstr = [itobin(int(c, 16)) for c in hexstr]
    return ''.join(binstr)


def sumver(str):
    if len(str) < 11:
        return 0
    sum = int(str[:3], 2)  # packet version
    if str[3:6] == '100':  # packet type
        body = str[6:]
        pos = 0
        while body[pos] == '1':
            pos += 5
        sum += sumver(body[pos+5:])
    else:
        type_id = int(str[6:7], 2)
        body = str[7:]
        if type_id == 0:
            sublen = int(body[:15], 2)
            sub, rest = body[15:15+sublen], body[15+sublen:]
            sum += sumver(sub)
            sum += sumver(rest)
        else:
            sum += sumver(body[11:])
    return sum


assert sumver(hextobin("8A004A801A8002F478")) == 16
assert sumver(hextobin("620080001611562C8802118E34")) == 12
assert sumver(hextobin("C0015000016115A2E0802F182340")) == 23
assert sumver(hextobin("A0016C880162017C3686B18A3D4780")) == 31

input = open('./input').read().strip()
binstr = hextobin(input)
print('Answer 1:', sumver(binstr))
