from functools import reduce


def itobin(x: int) -> str:
    return format(x, '04b')


def hextobin(hexstr: str) -> str:
    binstr = [itobin(int(c, 16)) for c in hexstr]
    return ''.join(binstr)


def evaluate(str):
    type = int(str[3:6], 2)

    # literal value
    if type == 4:
        body = str[6:]
        read = 0
        bin = ''
        while True:
            last = body[read] == '0'
            bin += body[read+1:read+5]
            read += 5
            if last:
                break
        read += 6  # header
        return (int(bin, 2), read)

    # operator packet
    else:
        type_id = int(str[6:7], 2)
        body = str[7:]
        nums = []
        read = 0
        if type_id == 0:
            bits = int(body[:15], 2)
            while read < bits:
                num, i = evaluate(body[15+read:15+bits])
                nums.append(num)
                read += i
            read += 22  # header
        else:
            packages = int(body[:11], 2)
            for _ in range(packages):
                num, i = evaluate(body[11+read:])
                nums.append(num)
                read += i
            read += 18  # header

        val = None
        if type == 0:
            val = sum(nums)
        elif type == 1:
            val = reduce(lambda x, y: x*y, nums)
        elif type == 2:
            val = min(nums)
        elif type == 3:
            val = max(nums)
        elif type == 5:
            val = int(nums[0] > nums[1])
        elif type == 6:
            val = int(nums[0] < nums[1])
        elif type == 7:
            val = int(nums[0] == nums[1])
        return (val, read)

input = open('./input').read().strip()
val, read = evaluate(hextobin(input))
print('Answer 2:', val)
