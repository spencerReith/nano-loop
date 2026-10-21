import subprocess


class Sandbox:
    def __init__(self, name):
        self.name = name
        subprocess.run(["docker", "run", "-d", "--name", self.name, "-w", "/work", "python:3.13-slim", "sleep", "infinity"], check=True)

    def kill(self):
        subprocess.run(["docker", "rm", "-f", self.name], capture_output=True)

    def write_file(self, path, content):
        subprocess.run(["docker", "exec", "-i", self.name, "sh", "-c", 'mkdir -p "$(dirname "$1")" && cat > "$1"', "_", path], input=content, text=True, check=True)
        return f"File written to {path}"

    def read_file(self, path):
        r = subprocess.run(["docker", "exec", self.name, "cat", path], capture_output=True, text=True)
        if r.returncode == 0:
            return f"stdout:\n {r.stdout}"
        else: return f"stderr:\n{r.stderr}"

    def run_python(self, path):
        r = subprocess.run(["docker", "exec", self.name, "python", path], capture_output=True, text=True)
        return f"stdout + stderr: {r.stdout + r.stderr}"
