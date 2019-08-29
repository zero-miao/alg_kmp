"""
求解模式串 p 的 next 数组.

    next[i] i>0
    求法: 是 p[0:i-1] 的前缀和后缀中, 最长的相等的字符串长度.
    用处: p[0:i-1]匹配, 但是 p[i] 不匹配时, 模式串向后移动 i-next[i] 位, 且从 p[next[i]] 开始比较.
    特殊情况: next[0] 默认是置为 0, 但是如果 p[0] 不匹配时, 应该向右移动 1 位, 而不是 0-0=0.(最少移动一位)
        或者 next[0] 置为 -1, 如果 p[0] 不匹配时, 应该向右移动 0-(-1)=1 位, 但是要从 0 开始比较.

example:

p = "abcbabc"
next[i]

index   0   1   2   3   4   5   6
alpha   a   b   c   b   a   b   c
next    0  0   0   0   0   1   2

c = abcbaxabcbabc
p = abcbabc

两个游标: i 指向 c, j 指向 p. c[i+j] 与 p[j] 比较. 右移则移动 i, 从第 j 个开始比较.

第一次不相等的 i, j
i   0   4   5   6   匹配成功
j   5   1   0   0
n5  1   0   -1
s   4   1   1
"""


def find_next(s, l):
    # 前缀后缀匹配的最大长度, 匹配前 l 个即可
    for length in range(l - 1, 0, -1):
        if s[:length] == s[l - length + 1:l + 1]:
            return length
    return 0


def kmp_next(s):
    """

    :param s: 需要求 next 的字符串 s.
    :return: 返回 next 数组.
    >>> kmp_next("abcbabc")
    [0, 0, 0, 0, 0, 1, 2]
    >>> kmp_next("ababababcbab")
    [0, 0, 0, 1, 2, 3, 4, 5, 6, 0, 0, 1]
    >>> kmp_next("abacabacd")
    [0, 0, 0, 1, 0, 1, 2, 3, 4]
    """
    n = [0]
    for i in range(1, len(s)):
        # 计算 next[i]
        n.append(find_next(s, i - 1))
    return n


def advance_next(s):
    """改进的 next 数组.

    p[j] 发生不匹配时, 已知 p[j] != s[i+j];
    新一轮比较为: 右移 j-n[j], 从第 n[j] 开始比较. 则对应 p[n[j]] 和 s[i+j]
    如果已知: p[n[j]] == p[j], 则这一轮的比较是没有意义的. (而 kmp 算法并没有注意这个)
        相等时, 跳过这一轮比较.
        n[j] = n[n[j]]

    :param s: 需要求 next 的字符串 s.
    :return: 返回 next 数组.
    >>> advance_next("abcbabc")
    [0, 0, 0, 0, 0, 0, 0]
    >>> advance_next("abcbabcd")
    [0, 0, 0, 0, 0, 0, 0, 3]
    >>> advance_next("ababcababcababcababc")
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2]
    """
    n = kmp_next(s)
    lp = len(s)
    for i in range(1, lp):
        # 计算 next[i]
        j = n[i]  # 新位置是 j
        while j > 0 and s[i] == s[j]:
            n[i] = n[j]
            j = n[i]
    return n


def index(c, p):
    """

    :param c: 待匹配的字符串
    :param p: 模式串
    :return: 返回匹配的位置的第一个字符在 c 中的索引. 以及比较的次数.
    >>> index("abcbaxabcbabc", "abcbabc")
    (6, 14)
    >>> index("abcbaxabcbabcd", "abcbabcd")
    (6, 15)
    >>> index("abcbaxabcbabcd", "abcbabcc")
    (-1, 15)
    >>> index("ababcababcababcababxababcababcababcabaxxababcababcababcababc", "ababcababcababcababc")
    (40, 63)
    """
    # n = kmp_next(p)
    n = advance_next(p)
    i, j = 0, 0
    lp = len(p)
    lc = len(c)
    count = 0
    while i <= lc - lp:
        # print(c)
        # print(" " * i + p)
        # print(" " * (i + j) + "^")
        if j >= lp:
            return i, count
        count += 1
        if c[i + j] == p[j]:
            j += 1
        else:
            step = j - n[j]
            if step <= 0:
                step = 1
            i += step
            j = n[j]
    return -1, count
