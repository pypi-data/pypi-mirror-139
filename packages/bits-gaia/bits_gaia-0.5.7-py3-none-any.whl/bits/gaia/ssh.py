# -*- coding: utf-8 -*-
"""Gaia SSH class file."""
import ast
import json
import logging
import os
import subprocess

SSH_DIR_PATH = "/root/.ssh"
SSH_KEY_PATH = f"{SSH_DIR_PATH}/gaia_id_dsa"
SSH_OPTIONS = f"-i {SSH_KEY_PATH} -oStrictHostKeyChecking=no"


class SSH:
    """Gaia SSH class."""

    def __init__(self, host, user, key, cli):
        """Initialize a class instance."""
        self.cli = cli
        self.host = host
        self.key = key
        self.user = user

        self.prepare_environment()

    def prepare_environment(self):
        """Prepare the linux environment to connect to SSH."""
        # create .ssh directory if it does not exist
        if not os.path.exists(SSH_DIR_PATH):
            os.mkdir(SSH_DIR_PATH, mode=0o700)

        # save ssh key to disk
        f = open(SSH_KEY_PATH, "w")
        f.write(self.key)
        f.close()

        # chmod the ssh key
        os.chmod(SSH_KEY_PATH, mode=0o700)

    def run_command(self, command):
        """Run a command on the on-prem SSH host."""
        base_command = f"ssh {SSH_OPTIONS} {self.user}@{self.host} env TERM=dumb"
        cmd = f"{base_command} {command}"
        try:
            return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()
        except Exception as err:
            logging.error(f"Failed to run SSH command: {cmd} [{err}]")
            raise err

    def run_bitsdbcli_command(self, command):
        """Run a bitsdb-cli command on the on-prem SSH host."""
        cmd = f"sudo /broad/devops/{self.cli}/bitsdb-cli/client {command}"
        output = self.run_command(cmd)

        lines = output.strip().split("\n")
        response = ast.literal_eval(lines[-1])
        print("\n".join(lines[:-1]))
        return response

    def run_bitsdbcli_command_with_json_response(self, command):
        """Run a bitsdb-cli command on the on-prem SSH host."""
        cmd = f"sudo /broad/devops/{self.cli}/bitsdb-cli/client {command}"
        print(f"Running: {cmd}")
        raw_response = self.run_command(cmd)
        try:
            response = json.loads(raw_response)
        except Exception as err:
            error = f"Failed to parse JSON response: {raw_response} [{err}]"
            return {"error": error}
        if "error" in response:
            error = f"Error received running bitsdb-cli command: {command} [{response['error']}]"
            return {"error": error}
        firestore_response = response.get("firestore", {})
        output = response.get("output", [])
        print("\n".join(output))
        return firestore_response
