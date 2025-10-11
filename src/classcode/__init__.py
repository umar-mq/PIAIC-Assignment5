import subprocess


def main():
    args = ["uv", "run", "chainlit", "run", "E:\\PIAIC-Assignment5\\src\\classcode\\app.py", "-w"]

    return subprocess.run(args).returncode
