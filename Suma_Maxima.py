import sys
from typing import TextIO


def read_data(f: TextIO) -> list[int]:
    return [int(l) for l in f.readlines()]


def process(v: list[int]) -> tuple[int, int, int]:
    def suma_maxima(b: int, e: int) -> tuple[int, int, int]:
        # Casos base
        if e <= b:
            return 0, b, e
        if e == b + 1:
            return v[b], b, e
        # Caso general
        m = (b + e) // 2
        si, bi, ei = suma_maxima(b, m)
        sd, bd, ed = suma_maxima(m, e)
        sp = 0
        sc1 = 0
        ec = m
        for i in range(m, e):
            sp += v[i]
            if sp > sc1:
                sc1 = sp
                ec = i + 1
        sc2 = 0
        sp = 0
        bc = b
        for i in range(m - 1, b - 1, -1):
            sp += v[i]
            if sp > sc2:
                sc2 = sp
                bc = i
        sc = sc1 + sc2
        # Opcion 1
        if sc > sd and sc > si:
            return sc, bc, ec
        if sd > sc and sd > si:
            return sd, bd, ed
        return si, bi, ei
        # Opcion 2
        return max((sc, bc, ec),(si, bi, ei),(sd, bd, ed))

    return suma_maxima(0, len(v))


def show_results(sm: int, b: int, e: int):
    print(sm)
    print(b)
    print(e)


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sm, b, e = process(v)
    show_results(sm, b, e)
