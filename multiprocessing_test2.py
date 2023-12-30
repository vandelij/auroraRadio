import multiprocessing
import subprocess
import time
import os

def run_script(script_path, process_id, child_processes):
    try:
        # Run the script in a separate process
        subprocess.run(['python3', script_path])
    except Exception as e:
        print(f"Process {process_id} error: {e}")
    finally:
        # Remove the child process ID from the list when the child process terminates
        child_processes.remove(os.getpid())

def terminate_children(child_processes):
    # Terminate all child processes
    for child_pid in child_processes:
        try:
            os.kill(child_pid, 15)  # SIGTERM signal
        except ProcessLookupError:
            pass  # Process already terminated

if __name__ == "__main__":
    script_path = "rtl_sdr_test.py"
    manager = multiprocessing.Manager()
    child_processes = manager.list()

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