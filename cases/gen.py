"""
quick n dirty test case gen. refs are checked against brute force on small inputs.
run: python cases/gen.py  -> writes cases/<problem>.json as [{"input": {...}, "expected": ...}]
"""
import json, random, itertools, pathlib
from collections import Counter, defaultdict

random.seed(0)
OUT = pathlib.Path(__file__).parent


# ---------- refs ----------
def sharp(nums):
    return sum(nums[i] == nums[i - 1] for i in range(1, len(nums)))

def sharp_brute(nums):
    n = len(nums)
    for d in range(n + 1):
        for drop in itertools.combinations(range(n), d):
            a = [x for i, x in enumerate(nums) if i not in drop]
            if all(a[i] ^ a[i + 1] for i in range(len(a) - 1)):
                return d

def max_product_pair(nums, target):
    # returns best product or None; multiple index answers are valid so check by product
    best = None
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] + nums[j] == target and nums[i] > nums[j]:
                p = nums[i] * nums[j]
                best = p if best is None else max(best, p)
    return best

def rearrange(nums):
    c, ans = Counter(nums), []
    while c:
        for v in sorted(c):
            ans.append(v)
            c[v] -= 1
            if not c[v]:
                del c[v]
    return ans

def equally_spaced(nums):
    pos = defaultdict(list)
    for i, x in enumerate(nums):
        pos[x].append(i)
    return sum(len(p) == 3 and p[1] - p[0] == p[2] - p[1] for p in pos.values())

def ascii_pal(s):
    b = "".join(format(ord(ch), "08b") for ch in s)
    return b == b[::-1]

def last_visited(grid):
    m, n = len(grid), len(grid[0])
    d = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}
    r = c = 0
    seen = {(0, 0)}
    while True:
        dr, dc = d[grid[r][c]]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < m and 0 <= nc < n) or (nr, nc) in seen:
            return [r, c]
        r, c = nr, nc
        seen.add((r, c))

def max_equal_adj(nums):
    base = sum(nums[i] == nums[i + 1] for i in range(len(nums) - 1))
    cnt = Counter(frozenset((nums[i], nums[i + 1])) for i in range(len(nums) - 1) if nums[i] != nums[i + 1])
    return base + max(cnt.values(), default=0)

def max_equal_adj_brute(nums):
    vals = set(nums)
    best = sum(nums[i] == nums[i + 1] for i in range(len(nums) - 1))
    for x in vals:
        for y in vals:
            if x != y:
                a = [y if v == x else v for v in nums]
                best = max(best, sum(a[i] == a[i + 1] for i in range(len(a) - 1)))
    return best

def transform(source, target):
    # op preserves sum, and with n>=2 any same-sum array is reachable
    return sum(source) == sum(target)

def transform_brute(source, target, lim=4):
    # bfs over small value range
    start, goal = tuple(source), tuple(target)
    seen, q = {start}, [start]
    while q:
        cur = q.pop()
        if cur == goal:
            return True
        for i in range(len(cur)):
            for j in range(len(cur)):
                if i == j:
                    continue
                for delta in range(-lim, lim + 1):
                    a = list(cur)
                    a[i] = cur[i] + cur[j] - delta
                    a[j] = delta
                    t = tuple(a)
                    if all(-lim <= v <= lim for v in t) and t not in seen:
                        seen.add(t)
                        q.append(t)
    return False

def good_rotations(nums):
    n, h = len(nums), len(nums) // 2
    total, a = sum(nums), nums + nums
    first = sum(a[:h])
    cnt = 0
    for r in range(n):
        cnt += first > total - first
        first += a[r + h] - a[r]
    return cnt

def good_rotations_brute(nums):
    n = len(nums)
    return sum(sum(r[:n // 2]) > sum(r[n // 2:]) for r in (nums[i:] + nums[:i] for i in range(n)))

def kth_digit(k):
    if k <= 9:
        return k
    k -= 9
    d = 2
    while k > 9 * 10 ** (d - 1) * d:
        k -= 9 * 10 ** (d - 1) * d
        d += 1
    off = k - 1
    n0 = 10 ** (d - 1) + off // d
    b, p = divmod(n0, 10)
    num = 10 * b + p if b % 2 == 0 else 10 * b + 9 - p
    return int(str(num)[off % d])

def kth_brute_string(limit):
    s, b = [], 0
    while len("".join(s)) < limit:
        nums = [x for x in range(10 * b, 10 * b + 10) if x > 0]
        if b % 2:
            nums.reverse()
        s += map(str, nums)
        b += 1
    return "".join(s)


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


# ---------- self checks ----------
for _ in range(300):
    a = [random.randint(1, 3) for _ in range(random.randint(2, 8))]
    assert sharp(a) == sharp_brute(a), a
    a = [random.randint(1, 4) for _ in range(random.randint(2, 9))]
    assert max_equal_adj(a) == max_equal_adj_brute(a), a
    a = rnd(2 * random.randint(1, 6), 1, 5)
    assert good_rotations(a) == good_rotations_brute(a), a
for _ in range(60):
    n = random.choice([2, 3])
    s = [random.randint(-2, 2) for _ in range(n)]
    t = [random.randint(-2, 2) for _ in range(n)]
    assert transform(s, t) == transform_brute(s, t), (s, t)
S = kth_brute_string(200000)
for k in range(1, 200000):
    assert kth_digit(k) == int(S[k - 1]), k
print("refs ok")


# ---------- cases ----------
def dump(name, cases):
    (OUT / f"{name}.json").write_text(json.dumps(cases))
    print(name, len(cases))

# sharp
c = [[1, 1, 2, 2, 2, 3], [4, 4, 9, 4], [1, 1], [1, 2], [5] * 100, list(range(1, 101))]
c += [rnd(random.randint(2, 100), 1, random.choice([2, 3, 100])) for _ in range(40)]
dump("minimum_deletions_to_make_array_sharp", [{"input": {"nums": a}, "expected": sharp(a)} for a in c])

# max product pair. expected_product = None means answer must be [-1,-1]
c = [([1, 2, 3, 4], 5), ([-3, -1, 4, 2], 1), ([3, 3, 5], 6), ([0, 0], 0), ([-100, 100], 0), ([50, 50, 50], 100)]
c += [(rnd(random.randint(2, 100), -100, 100), random.randint(-100, 100)) for _ in range(40)]
c += [(rnd(random.randint(2, 20), -5, 5), random.randint(-5, 5)) for _ in range(20)]
dump("maximum_product_pair_with_target_sum",
     [{"input": {"nums": a, "target": t}, "expected_product": max_product_pair(a, t),
       "note": "any [i,j] valid w/ max product ok; [-1,-1] if expected_product is null"} for a, t in c])

# rearrange
c = [[3, 1, 3, 2, 1, 3], [7, 7, 4, 4, 4], [1], [100] * 100, list(range(100, 0, -1))]
c += [rnd(random.randint(1, 100), 1, random.choice([3, 10, 100])) for _ in range(40)]
dump("rearrange_array_by_removing_distinct_values", [{"input": {"nums": a}, "expected": rearrange(a)} for a in c])

# equally spaced
c = [[1, 8, 1, 5, 1, 5, 8, 5], [8, 8, 8, 8], [8, 6, 6, 8, 8], [1, 1, 1], [1, 2, 3], [1, 2, 1, 2, 1, 2]]
c += [rnd(random.randint(3, 100), 1, random.choice([3, 10, 30])) for _ in range(40)]
for _ in range(10):  # plant some special values
    a = rnd(60, 10, 40)
    i, g = random.randint(0, 20), random.randint(1, 19)
    for k in range(3):
        a[i + k * g] = 1
    c.append(a)
dump("count_values_with_equally_spaced_occurrences_i", [{"input": {"nums": a}, "expected": equally_spaced(a)} for a in c])

# ascii pal
L = "abcdefghijklmnopqrstuvwxyz"
pal_chars = [ch for ch in L if format(ord(ch), "08b") == format(ord(ch), "08b")[::-1]]
c = ["ff", "leet", "a", "f", "z" * 100]
c += ["".join(random.choice(L) for _ in range(random.randint(1, 100))) for _ in range(20)]
# char x pairs with char whose bits are reversed; build true cases
rev = {ch: chr(int(format(ord(ch), "08b")[::-1], 2)) for ch in L}
mirror = [ch for ch in L if rev[ch] in L]
for _ in range(15):
    half = [random.choice(mirror) for _ in range(random.randint(1, 50))]
    mid = [random.choice(pal_chars)] if pal_chars and random.random() < 0.5 else []
    c.append("".join(half + mid + [rev[ch] for ch in reversed(half)]))
dump("check_ascii_palindromic", [{"input": {"s": s}, "expected": ascii_pal(s)} for s in c])

# last visited
def snake(m, n):
    g = [["R" if r % 2 == 0 else "L"] * n for r in range(m)]
    for r in range(m - 1):
        g[r][n - 1 if r % 2 == 0 else 0] = "D"
    return g
c = [[["R", "D"], ["U", "L"]], [["R", "R", "R"]], [["U"]], [["D"]] * 5, snake(316, 316), snake(1, 100000), [["D"]] * 100000]
c += [[[random.choice("LRUD") for _ in range(n)] for _ in range(m)] for m, n in [(random.randint(1, 8), random.randint(1, 8)) for _ in range(40)]]
for _ in range(5):  # snake w/ random noise -> long but not trivial paths
    g = snake(200, 200)
    for _ in range(50):
        g[random.randrange(200)][random.randrange(200)] = random.choice("LRUD")
    c.append(g)
dump("last_visited_cell_in_a_directional_grid", [{"input": {"grid": g}, "expected": last_visited(g)} for g in c])

# max equal adj
c = [[1, 2, 3, 2], [1, 2, 1, 2, 1], [1, 1, 1], [1, 2], [5, 5], [10**9, 1] * 50000, rnd(100000, 1, 10**9), rnd(100000, 1, 5)]
c += [rnd(random.randint(2, 30), 1, random.choice([2, 4, 10])) for _ in range(40)]
dump("maximum_equal_adjacent_pairs_after_at_most_one_replacement", [{"input": {"nums": a}, "expected": max_equal_adj(a)} for a in c])

# transform
c = [([1, 2, 3], [0, 2, 4]), ([-5, -5], [-15, 5]), ([1, 2, 1], [0, 2, 5]), ([0, 0], [0, 0]),
     ([10**9] * 100000, [-10**9] * 100000), ([10**9] * 100000, [10**9] * 99999 + [10**9 - 1])]
for _ in range(30):
    n = random.randint(2, 50)
    s = rnd(n, -10**9, 10**9)
    t = rnd(n, -10**9, 10**9)
    if random.random() < 0.5:
        t[-1] += sum(s) - sum(t)  # might push out of range, fine-ish; clamp by retry
        if not -10**9 <= t[-1] <= 10**9:
            t[-1] -= sum(s) - sum(t)
    c.append((s, t))
dump("transform_array_using_pair_operations", [{"input": {"source": s, "target": t}, "expected": transform(s, t)} for s, t in c])

# kth digit
c = [4, 15, 11, 1, 9, 10, 189, 190, 2889, 2890, 10**15, 10**15 - 1, 10**12 + 7]
c += [random.randint(1, 1000) for _ in range(20)] + [random.randint(1, 10**15) for _ in range(30)]
dump("k_th_digit_in_infinite_string", [{"input": {"k": k}, "expected": kth_digit(k)} for k in c])

# good cyclic rotations
c = [[1, 2, 3, 4, 5, 6], [1, 2, 1, 2], [1, 1], [1, 2], [2, 1], [10**9] * 100000, rnd(100000, 1, 10**9), rnd(100000, 1, 2)]
c += [rnd(2 * random.randint(1, 50), 1, random.choice([2, 10, 10**9])) for _ in range(40)]
dump("count_good_cyclic_rotations", [{"input": {"nums": a}, "expected": good_rotations(a)} for a in c])
