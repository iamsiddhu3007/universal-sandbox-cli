import docker
import click
import sys
import os
import subprocess

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