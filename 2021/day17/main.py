test_target = [[20, 30], [-10, -5]]
target = [[144, 178], [-100, -76]]


def check(target, vx, vy):
    x, y, max_y, it = 0, 0, 0, 0
    while True:
        x += vx
        y += vy
        if y > max_y:
            max_y = y
        if target[0][0] <= x <= target[0][1] and target[1][0] <= y <= target[1][1]: 
            return max_y
        if x > target[0][1] or y < target[1][0]:
            return None
        if vx > 0:
            vx -= 1
        vy -= 1
        it += 1
        if it > 1000: # circuit breaker
            return None 


def check_all(target):
    max_y = 0
    iv = 0
    # cpu goes brrrrrr
    for vx in range(1, 1000):
        for vy in range(-1000, 1000):
            y = check(target, vx, vy)
            if y != None:
                iv += 1
                if y > max_y:
                    max_y = y
    return max_y, iv


max_y, iv = check_all(target)
print('Answer 1:', max_y)
print('Answer 2:', iv)