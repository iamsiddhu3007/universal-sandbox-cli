import docker
import click
import sys
import os
import subprocess
import platform


def ensure_docker():
    """Checks if Docker is running. Opens it if closed, or exits if missing."""
    # 1. Check if Docker daemon is already active and responding
    try:
        client = docker.from_env()
        client.ping()
        return
    except (docker.errors.DockerException, Exception):
        pass

    os_name = platform.system()
    
    # 2. Check if Docker is installed on the machine at all
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True, text=True)
        is_installed = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        is_installed = False

    # 3. If missing, exit with a clear message
    if not is_installed:
        click.echo("\n[x] Error: Docker is not installed.")
        click.echo("[!] Universal Sandbox requires Docker to run the isolated Linux environment.")
        click.echo("[->] Please install Docker (or OrbStack on macOS) and try again.\n")
        sys.exit(1)

    # 4. If installed but closed, attempt to open it
    click.echo("[*] Docker is installed but not running. Launching Docker...")
    
    try:
        if os_name == "Darwin":
            subprocess.run(["open", "-a", "Docker"], check=True)
        elif os_name == "Windows":
            subprocess.run(["start", "docker"], shell=True, check=True)
        elif os_name == "Linux":
            subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
        
        click.echo("[*] Please wait a few seconds for Docker to boot up, then re-run your command.")
        sys.exit(0)
    except Exception as e:
        click.echo(f"[!] Could not launch Docker automatically: {e}")
        click.echo("[->] Please open Docker manually and try again.")
        sys.exit(1)


class SandboxManager:
    def __init__(self, image="iamsiddhu3007/universal-sandbox:latest"):
        self.client = docker.from_env()
        self.image = image
        self.container = None

    def start(self):
        click.echo("[*] Booting ephemeral AI sandbox...")
        current_mac_dir = os.getcwd()
        
        self.container = self.client.containers.run(
            self.image,
            command="tail -f /dev/null",
            detach=True,
            network_mode="bridge",
            mem_limit="1g",
            volumes={current_mac_dir: {'bind': '/workspace', 'mode': 'rw'}},
            working_dir="/workspace"
        )
        click.echo(f"[+] Sandbox active (ID: {self.container.id[:8]})")
        click.echo(f"[+] Mounted Mac folder: {current_mac_dir} -> /workspace\n")

    def execute(self, cmd):
        click.echo(f"[*] Executing command in background: {cmd}")
        exec_log = self.container.exec_run(f"bash -c '{cmd}'")
        return exec_log.output.decode("utf-8").strip()

    def interactive(self):
        click.echo("[*] Dropping into interactive Linux shell. Type 'exit' to leave.")
        subprocess.call(["docker", "exec", "-it", self.container.id, "bash"])

    def stop(self):
        if self.container:
            click.echo("\n[*] Tearing down sandbox...")
            self.container.remove(force=True)
            click.echo("[+] Sandbox destroyed. Nothing installed in the Host.")


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def main(command):
    """Run commands inside the universal AI sandbox, or boot into it interactively."""
    ensure_docker()
    manager = SandboxManager()
    
    try:
        manager.start()
        
        if command:
            # If the user passed a command (e.g., universal-sandbox-cli python3 --version)
            cmd_str = " ".join(command)
            output = manager.execute(cmd_str)
            click.echo("\n--- Output ---\n")
            click.echo(output)
            click.echo("\n--------------")
        else:
            # If the user just typed the package name, boot into Linux
            manager.interactive()
            
    finally:
        manager.stop()

if __name__ == "__main__":
    main()