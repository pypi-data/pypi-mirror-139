__author__ = "bosiic_m"

import os.path
import sys
from clrprint import *
import paramiko
import argparse
import logging
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Todos file', required=True)
    parser.add_argument('-i', help='Inventory file', required=True)
    args = parser.parse_args()

    with open(args.f, "r") as stream:
        todo = yaml.safe_load(stream)

    with open(args.i, "r") as stream:
        inventory = yaml.safe_load(stream)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for key, value in inventory['hosts']['webserver'].items():
        if key == "ssh_address":
            ip = value

        if key == "user_name":
            username = value

        if key == "password":
            password = value

        if key == "key_file" and value == 0:
            ssh.connect(ip, username=username, password=password)
            logging.warning("ok- simple ssh connection")

        if key == "key_file" and value == 1:
            ssh.connect(ip, username=username, password=password,
                        key_filename=os.path.join(os.path.expanduser('~'),
                                                  ".ssh", "id_ed25519"))
            logging.warning("ok- shh with keyfile connection")

    for i in range(len(todo)):
        for key, value in todo[i].items():
            if key == "module" and value == "service":
                service = todo[i]['params']['name']
                state = todo[i]['params']['state']

                if state == "enabled":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("sudo bash -c \"" +
                                         "systemctl enable " +
                                         service + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

                elif state == "started":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("sudo bash -c \"" +
                                         "systemctl start " +
                                         service + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

                elif state == "restarted":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("sudo bash -c \"" +
                                         "systemctl restart " +
                                         service + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

                elif state == "stopped":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("sudo bash -c \"" +
                                         "systemctl stop " +
                                         service + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

                elif state == "disabled":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("sudo bash -c \"" +
                                         "systemctl disable " +
                                         service + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

            if key == "module" and value == "command":
                command = todo[i]['params']['command']
                if len(todo[i]['params']) == 1:
                    shell = "bash"
                elif len(todo[i]['params']) == 2:
                    shell = todo[i]['params']['shell']

                session = ssh.get_transport().open_session()
                session.set_combine_stderr(True)
                session.get_pty()

                session.exec_command("sudo "+shell+" -c \"" + command + "\"")

                stdin = session.makefile('wb', -1)
                stdout = session.makefile('rb', -1)
                stderr = session.makefile('rb', -1)
                stdin.write(password + '\n')
                stdin.flush()

                logging.warning(stdout.read().decode().strip())
                logging.error(stderr.read().decode().strip())

            if key == "module" and value == "apt":
                application = todo[i]['params']['name']
                applicationstate = todo[i]['params']['state']

                if applicationstate == "present":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("yes | sudo bash -c \"" +
                                         "apt-get install " +
                                         application + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

                elif applicationstate == "absent":
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()

                    session.exec_command("yes | sudo \"" +
                                         "apt remove " + application + "\"")

                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stderr = session.makefile('rb', -1)
                    stdin.write(password + '\n')
                    stdin.flush()

                    logging.warning(stdout.read().decode().strip())
                    logging.error(stderr.read().decode().strip())

            if key == "module" and value == "copy":
                source = todo[i]['params']['src']
                destination = todo[i]['params']['dest']

                session = ssh.get_transport().open_session()
                session.set_combine_stderr(True)
                session.get_pty()

                session.exec_command("cp " + source + " " + destination)

                stdin = session.makefile('wb', -1)
                stdout = session.makefile('rb', -1)
                stderr = session.makefile('rb', -1)
                stdin.write(password + '\n')
                stdin.flush()

                logging.warning(stdout.read().decode().strip())
                logging.error(stderr.read().decode().strip())

    session.close()
    ssh.close()


main()
