import sys
import subprocess
import random
import tempfile
from a7d import Archive
from pathlib import Path


def test_using_tester_dir(tester_dir, context=None):
    if not isinstance(tester_dir, Archive):
        tester_dir = Archive(tester_dir)
    with tempfile.TemporaryDirectory() as test_dir:
        test_dir = Path(test_dir)
        if context is not None:
            context.to_directory(test_dir)
        tester_dir.to_directory(test_dir)
        result = subprocess.run(test_dir / "test", cwd=test_dir).returncode
    return result


def check_all_tests(tests, context=None, log=lambda x: print(x)):
    results = [0, 0]
    tests = list(Archive(tests).iterdir())
    if context is not None and not isinstance(context, Archive):
        context = Archive(context)
    for i, (name, test) in enumerate(tests):
        n = i + 1
        log(f"[{n}/{len(tests)}] {name}")
        result = test_using_tester_dir(test, context)
        results[result != 0] += 1
        result = "ok" if result == 0 else f"FAIL({result})"
        log(f"[{n}/{len(tests)}] -> {result}")
    return tuple(results)


def main():
    srcs = sys.argv[1:] or ["tests", "tests.a7d", "TESTS", "TESTS.a7d"]
    for tests in map(Path, srcs):
        if tests.is_dir() or tests.is_file():
            break
    else:
        raise Exception('"tests" directory is not found')
        return
    ok, fails = check_all_tests(tests, ".")
    total = ok + fails
    success_rate = ok / total if total else 1.0
    print(f"ok: {ok}")
    print(f"fails: {fails}")
    print(f"{100*success_rate:0.4}% passed")


if __name__ == "__main__":
    main()
