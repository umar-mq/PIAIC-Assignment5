import subprocess


def main():
    args = ["uv", "run", "chainlit", "run", "/home/mragi/PIAIC/classcode/src/classcode/app.py", "-w"]

    return subprocess.run(args).returncode
