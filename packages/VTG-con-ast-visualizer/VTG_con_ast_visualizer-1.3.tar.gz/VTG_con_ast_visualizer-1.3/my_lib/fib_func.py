def fib(n):
    if n == 1:
        return [0]
    ans = [0, 1]
    for i in range(n - 2):
        ans.append(ans[-1] + ans[-2])
    return ans
