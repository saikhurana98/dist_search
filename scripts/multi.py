from multiprocessing import pool
import os
import sys


def execute_commands(cmds):
    # cmds is a list of you need to execute
    # in your case, it could be filenames
    # do something with it here
    return 0

def func():
    def chunks(l, n):
        lst = []
        for i in range(0, len(l), n):
            lst.append(l[i : i + n])
        return lst
    commands = []
    # write code to populate the commands here
    # in your case, command can be file names
    p = pool.Pool(16)
    cmd_chunks = chunks(commands, 100)
    p.map(execute_commands, cmd_chunks)
    p.terminate()

if __name__ == "__main__":
    func()
