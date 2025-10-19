import subprocess


def main():
    args = ["uv", "run", "chainlit", "run", "./src/classcode/app.py", "-w"]

    return subprocess.run(args).returncode
