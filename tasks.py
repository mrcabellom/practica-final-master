"""Task runner. Works the same on Windows, macOS and Linux.

    python tasks.py              list the tasks
    python tasks.py run          run the pipeline over data/inbox
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable
DELIVERIES = {1: "KIV-101", 2: "KIV-102"}


def _module(*args):
    env = {**os.environ, "PYTHONUTF8": "1"}  # correct accents on Windows too
    return subprocess.call([PYTHON, "-m", *args], cwd=ROOT, env=env)


def setup(_):
    """Check the environment."""
    if sys.version_info < (3, 11):
        print("Hace falta Python 3.11 o superior.")
        return 1
    missing = []
    for module in ("pytest", "tzdata"):
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    if missing:
        print(f"Faltan dependencias: {', '.join(missing)}. Ejecuta: uv sync")
        return 1
    print(f"Python {sys.version.split()[0]} OK. Dependencias OK.")
    return 0


def run(_):
    """Run the pipeline: data/inbox -> output/."""
    return _module("kivora")


def test(_):
    """Run the tests."""
    return _module("pytest", "-q")


def check(_):
    """Basic checks on output/."""
    return _module("kivora.check")


def reset(_):
    """Delete output/."""
    target = ROOT / "output"
    if target.exists():
        shutil.rmtree(target)
        print("Borrado output/")
    else:
        print("Nada que borrar.")
    return 0


def deliver(args):
    """Simulate the shop: drop delivery N in data/inbox/ and its ticket in docs/tickets/."""
    n = args.n
    if n not in DELIVERIES:
        print(f"No hay entrega {n}: son la 1 y la 2.")
        return 1
    if n == 2 and not (ROOT / "docs" / "tickets" / f"{DELIVERIES[1]}.md").exists():
        print("Antes de la entrega 2 hay que recibir la 1: python tasks.py deliver 1")
        return 1
    source = ROOT / "deliveries" / f"delivery-{n}"
    inbox = ROOT / "data" / "inbox"
    ticket = DELIVERIES[n]
    if not (source / f"{ticket}.md").exists():
        print(f"Falta {source.relative_to(ROOT)}/{ticket}.md: la entrega está incompleta.")
        return 1
    days = sorted(p for p in source.iterdir() if p.is_dir())
    for day in days:
        target = inbox / day.name
        if target.exists():
            print(f"{target.relative_to(ROOT)} ya existe: la entrega {n} ya se había recibido.")
            return 1
    for day in days:
        shutil.copytree(day, inbox / day.name)
    shutil.copy(source / f"{ticket}.md", ROOT / "docs" / "tickets" / f"{ticket}.md")
    print(f"Entregados {len(days)} días en data/inbox/ ({days[0].name} .. {days[-1].name})")
    print(f"Nuevo ticket: docs/tickets/{ticket}.md")
    return 0


TASKS = {
    "setup": setup,
    "run": run,
    "test": test,
    "check": check,
    "reset": reset,
    "deliver": deliver,
}


def main():
    parser = argparse.ArgumentParser(description="Tareas del proyecto.")
    sub = parser.add_subparsers(dest="task")
    for name, function in TASKS.items():
        command = sub.add_parser(name, help=function.__doc__)
        command.set_defaults(function=function)
        if name == "deliver":
            command.add_argument("n", type=int, help="número de entrega (1 o 2)")
    args = parser.parse_args()
    if args.task is None:
        parser.print_help()
        return 0
    os.chdir(ROOT)
    sys.stdout.reconfigure(encoding="utf-8")
    return args.function(args)


if __name__ == "__main__":
    sys.exit(main())
