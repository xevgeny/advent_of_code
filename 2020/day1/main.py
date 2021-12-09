
lines = open('./input', 'r').read().split('\n')
nums = [int(x) for x in lines]

def product_of_2(nums):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == 2020:
                return nums[i] * nums[j]

def product_of_3(nums):
    for i in range(len(nums)):
        for j in range(len(nums)):
            for k in range(len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    return nums[i] * nums[j] * nums[k]

print('Answer 1: {}'.format(product_of_2(nums)))
print('Answer 2: {}'.format(product_of_3(nums)))
