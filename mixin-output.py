#!/usr/bin/env python3

import pathlib
import subprocess
import typing

def parse(path: pathlib.Path) -> typing.Iterator[str]:
    with open(path) as f:
        do_print = False
        block = ""
        for line in f:
            line = line.rstrip()
            if all(c == '-' for c in line) and len(line) >= 3:
                do_print = not do_print
                yield (("prose" if do_print else "code"), block)
                block = ""
            else:
                block += f"{line}\n"

def match_previous(old, new):
    assert old == new[:len(old)]
    return (new, new[len(old):])

def main():
    noq = pathlib.Path("./Noq/target/release/noq")
    target = pathlib.Path("./derivative.adoc")
    assert noq.exists(), "Build Noq interpreter in release mode first"

    previous_input, previous_stderr, previous_stdout = "", "", ""

    for ty, content in parse(target):
        match ty:
            case "prose":
                print(content, end="")
            case "code":
                print("----")
                print(content.rstrip())
                print("----")

                proc = subprocess.Popen([noq], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                previous_input += content

                stdout, stderr = proc.communicate(previous_input.encode('utf-8'))
                stderr = stderr.decode('utf-8')
                stdout = stdout.decode('utf-8')
                previous_stderr, stderr = match_previous(previous_stderr, stderr)
                previous_stdout, stdout = match_previous(previous_stdout, stdout)

                print(".Noq output")
                print("[%collapsible]")
                print("=====")
                print("Standard output:")
                print("[source]")
                print("----")
                print(stdout.rstrip())
                print("----\n")
                print("Standard error:")
                print("[source]")
                print("----")
                print(stderr.rstrip())
                print("----")
                print("=====")


if __name__ == "__main__":
    main()
