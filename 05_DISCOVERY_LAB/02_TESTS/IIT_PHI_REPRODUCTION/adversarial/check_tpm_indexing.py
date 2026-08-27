#!/usr/bin/env python3
"""
Independent (from-scratch) verification of the TPM encoding claimed in
PREREGISTRATION.md for A=OR(B,C), B=AND(A,C), C=XOR(A,B).

We do NOT read the front's reproduce_phi.py. We derive, by hand, what the
state-by-node TPM should look like under both plausible node<->bit index
conventions (LOLI: node 0 = least-significant bit; HOLI: node 0 =
most-significant bit), and compare against the TPM given in the
pre-registration:

TPM = [[0,0,0],[0,0,1],[1,0,1],[1,0,0],[1,0,0],[1,1,1],[1,0,1],[1,1,0]]

Row index i (0..7) is supposed to encode a current state of (A,B,C); each
row gives (A_next, B_next, C_next) deterministically.
"""

given_tpm = [
    [0, 0, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]

def next_state(a, b, c):
    a_next = int(b or c)          # A = OR(B,C)
    b_next = int(a and c)         # B = AND(A,C)
    c_next = int(bool(a) != bool(b))  # C = XOR(A,B)
    return (a_next, b_next, c_next)

def build_tpm(convention):
    """convention: 'loli' -> node0(A) is LSB; 'holi' -> node0(A) is MSB."""
    tpm = [None] * 8
    for i in range(8):
        if convention == 'loli':
            a = (i >> 0) & 1
            b = (i >> 1) & 1
            c = (i >> 2) & 1
        elif convention == 'holi':
            a = (i >> 2) & 1
            b = (i >> 1) & 1
            c = (i >> 0) & 1
        else:
            raise ValueError(convention)
        tpm[i] = list(next_state(a, b, c))
    return tpm

for convention in ('loli', 'holi'):
    tpm = build_tpm(convention)
    match = (tpm == given_tpm)
    print(f"=== convention={convention} match_given_tpm={match} ===")
    for i in range(8):
        if convention == 'loli':
            a, b, c = (i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1
        else:
            a, b, c = (i >> 2) & 1, (i >> 1) & 1, (i >> 0) & 1
        print(f"  row {i}: state(A,B,C)=({a},{b},{c}) -> derived={tpm[i]}  given={given_tpm[i]}  {'OK' if tpm[i]==given_tpm[i] else 'MISMATCH'}")
    print()

print("Given TPM:", given_tpm)
