#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
import glob
from io import StringIO
import os
import re
import sys
from time import process_time
import traceback
from typing import Any

from e2 import read_data, process, show_results, Problem, Reservation, Forecast


if sys.version_info.major != 3 or sys.version_info.minor < 10:
    raise RuntimeError("This program needs Python3, version 3.10 or higher")


INPUT = ".i"
OUTPUT = ".o"


TestPaths = tuple[str, str]
Test = tuple[Problem, Forecast]


def error(msg: str, exc_info=None):
    print()
    print("ERROR. " + msg, file=sys.stderr)
    if exc_info != None:
        for line in traceback.format_exception(*exc_info):
            if 'e2_test.py' not in line:
                sys.stderr.write(line)
    exit()


def natural_sort(l: list):
    num = re.compile("([0-9]+)")
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split(num, key)]
    l.sort(key=alphanum_key)


def retrieve_test_paths(opts: Namespace) -> list[TestPaths]:
    inputs = []
    if opts.directory is not None:
        inputs = glob.glob(opts.directory + "/*" + INPUT)
    inputs.extend(opts.tests)
    natural_sort(inputs)
    paths = []
    for fin in inputs:
        nin, ein = os.path.splitext(fin)
        fout = nin + OUTPUT
        if ein != INPUT:
            error(f"El fichero de entrada {fin} no tiene la extensión {INPUT}")
        if not os.path.exists(fin):
            error(f"El fichero {fin} no existe")
        if not os.path.exists(fout):
            error(f"El fichero {fout} no existe")
        paths.append((fin, fout))
    return paths


def read_tests(paths: list[TestPaths]) -> list[Test]:
    tests = []
    for fin, fout in paths:
        try:
            with open(fin) as f:
                try:
                    problem = read_data(f)
                except Exception as e:
                    error(f"Tu función read_data() ha lanzado una excepción al leer el archivo '{fin}'", sys.exc_info())
        except Exception as e:
            error(f"Excepción al leer el archivo '{fin}'", sys.exc_info())

        try:
            with open(fout) as f:
                forecast = [int(n) for n in f.readline().split()]
        except Exception as e:
            error(f"Excepción al leer el archivo '{fout}'", sys.exc_info())
        tests.append((problem, forecast))
    return tests


def check_process(paths: list[TestPaths], tests: list[Test], opts: Namespace):
    for (fin, _), (problem, forecast) in zip(paths, tests):
        if opts.verbose:
            print(f"Probando: {fin}", end="")
        try:
            t0 = process_time()
            candidate = process(problem)
            t1 = process_time()
        except Exception as e:
            error(f"Tu función process() ha lanzado una excepción en la prueba {fin}", sys.exc_info())
        if candidate == forecast:
            total_time = t1 - t0
            if total_time <= opts.timeout:
                if opts.verbose:
                    print(f" --> OK, tiempo: {total_time:.4f}")
            else:
                error(f"Timeout con la prueba {fin}, tiempo total: {total_time:.4f}")
        else:
            error_in_candidate(fin, candidate, problem, forecast)
    print("Todas las pruebas de process() han sido correctas")


def error_in_candidate(fin: str, candidate: Any, problem: Problem, forecast: Forecast):
    if not isinstance(candidate, list):
        error(f"Tu función process() no ha devuelto una lista en la prueba {fin}")
    if not candidate:
        error(f"Tu función process() ha devuelto una lista vacía en la prueba {fin}")
    if any(not isinstance(n, int) for n in candidate):
        error(f"Tu función process() ha devuelto una lista con algún elemento no entero en la prueba {fin}")
    for i in range(min(len(candidate), len(forecast))):
        ci = candidate[i]
        pi = forecast[i]
        if i % 2 == 0:
            t = pi
        if ci != pi:
            if i % 2 == 0:
                error(f"En la prueba {fin}, tu función process() ha devuelto la marca de tiempo {ci} en la posición {i} cuando debería haber devuelto {pi}")
            else:
                rs = busca_momento(t, problem[1])
                error(f"En la prueba {fin}, tu función process() ha devuelto {ci} habitaciones en la posición cuando deberían ser {pi} correspondientes a las reservas {rs}")
    if len(candidate) < len(forecast):
        error(f"En la prueba {fin}, tu función process() ha devuelto una previsión más corta de lo esperado")
    if len(candidate) > len(forecast):
        error(f"En la prueba {fin}, tu función process() ha devuelto una previsión más larga de lo esperado")


def busca_momento(m: int, reservations: list[Reservation]) -> str:
    rs = []
    for t, p, d in reservations:
        if t <= m < t+d:
            rs.append((t, p, d))
    return str(rs)


def main():
    parser = ArgumentParser(prog="e2_test",
                            description="Prueba del entregable 2")
    parser.add_argument("-d", "--directory",
                        help="Directorio con pruebas", type=str)
    parser.add_argument("-t", "--timeout", default=1, type=float)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("tests", nargs="*")
    opts = parser.parse_args()
    paths = retrieve_test_paths(opts)
    tests = read_tests(paths)
    check_process(paths, tests, opts)


if __name__ == "__main__":
    main()

