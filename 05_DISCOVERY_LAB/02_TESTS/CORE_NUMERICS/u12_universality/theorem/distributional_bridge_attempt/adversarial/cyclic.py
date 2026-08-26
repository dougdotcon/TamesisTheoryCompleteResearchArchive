"""Shared helper: exact cyclic-point detection for a functional digraph f:[n]->[n] (0-indexed)."""

def cyclic_mask(f):
    """f: list of length n, f[i] in range(n). Returns list of bool, cyclic_mask[i]=True iff i is cyclic."""
    n = len(f)
    state = [0]*n  # 0=unvisited,1=on current stack,2=done
    cyclic = [False]*n
    for start in range(n):
        if state[start] != 0:
            continue
        stack = []
        pos = {}
        cur = start
        while True:
            if state[cur] == 0:
                pos[cur] = len(stack)
                stack.append(cur)
                state[cur] = 1
                cur = f[cur]
            elif state[cur] == 1:
                # found a new cycle: stack[pos[cur]:] is the cycle
                p = pos[cur]
                for x in stack[p:]:
                    cyclic[x] = True
                for x in stack:
                    state[x] = 2
                break
            else:  # state[cur]==2, done already (cyclic or not, doesn't matter)
                for x in stack:
                    state[x] = 2
                break
    return cyclic


def count_cyclic(f):
    return sum(cyclic_mask(f))
