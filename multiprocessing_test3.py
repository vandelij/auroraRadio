import multiprocessing
import subprocess
import time
import os
import signal

class ChildProcess:
    def __init__(self, process, pid):
        self.process = process
        self.pid = pid

def run_script(script_path, process_id, child_processes):
    try:
        # Run the script in a separate process
        process = subprocess.Popen(['python', script_path], preexec_fn=os.setsid)
        child = ChildProcess(process, process.pid)
        child_processes.append(child)

        # Wait for the process to finish
        process.communicate()
    except Exception as e:
        print(f"Process {process_id} error: {e}")
    finally:
        print(f"Child process {child.pid} terminated.")
        child_processes.remove(child)

def terminate_children(child_processes):
    # Terminate all child processes
    for child in child_processes:
        try:
            os.killpg(os.getpgid(child.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass  # Process already terminated

if __name__ == "__main__":
    script_path = "rtl_sdr_test.py"
    child_processes = []

    # Start the script in a separate process
    process = multiprocessing.Process(target=run_script, args=(script_path, os.getpid(), child_processes))

    # Start the process
    process.start()

    try:
        # Let the process run for some time (you can adjust this)
        time.sleep(5)

        # Terminate the process and its children
        process.terminate()
        process.join()

        # Terminate any remaining children
        terminate_children(child_processes)

        print(f"Process {process.pid} terminated along with its children.")
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print(f"Keyboard interrupt received. Terminating process {process.pid} and its children.")
        process.terminate()
        process.join()

        # Terminate any remaining children
        terminate_children(child_processes)