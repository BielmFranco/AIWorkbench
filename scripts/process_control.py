"""Bound subprocess trees used by adapters, graders and candidate workers."""
import os
import signal
import subprocess


def terminate_tree(process, job=None):
    if job is not None:
        job.close()
    elif os.name != "nt":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()
    process.wait(timeout=5)


def run_bounded(command, *, timeout, input=None, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=None, env=None):
    job = None
    if os.name == "nt":
        from windows_job import WindowsJob
        job = WindowsJob()
    process = None
    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE if input is not None else stdin, stdout=stdout, stderr=stderr, cwd=cwd, env=env, text=True, encoding="utf-8", start_new_session=os.name != "nt", creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP | 0x4) if os.name == "nt" else 0)
        if job is not None:
            job.assign_and_resume(process)
        output, errors = process.communicate(input=input, timeout=timeout)
        return subprocess.CompletedProcess(command, process.returncode, output, errors)
    finally:
        if process is not None:
            terminate_tree(process, job)
            process.communicate(timeout=5)
        elif job is not None:
            job.close()
