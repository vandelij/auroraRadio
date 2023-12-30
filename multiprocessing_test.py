import multiprocessing
import subprocess
import time
import os

def run_script(script_path, process_id):
    try:
        # Run the script in a separate process
        subprocess.run(['python3', script_path])
    except Exception as e:
        print(f"Process {process_id} error: {e}")

if __name__ == "__main__":
    script_path = "rtl_sdr_test.py"

    # Start the script in a separate process
    process = multiprocessing.Process(target=run_script, args=(script_path, os.getpid()))

    # Start the process
    print(f'Starting process {process.pid}')
    process.daemon = True
    process.start()

    try:
        # Let the process run for some time (you can adjust this)
        print('Waiting 5 seconds.')
        time.sleep(5)
        print('Killing process')

        #stop_signal = input("Press any key to stop the recording")

        # Terminate the process
        process.terminate()
        process.join()  # Wait for the process to finish

        print(f"Process {process.pid} terminated.")
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print(f"Keyboard interrupt received. Terminating process {process.pid}.")
        process.terminate()
        process.join()