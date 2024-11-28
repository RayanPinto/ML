import subprocess
import threading
import time
import multiprocessing

# To run Jarvis
def startJarvis():
    # Code for process 1
    print("Process 1 is running.")
    from main import start
    start()

# To run hotword
def listenHotword():
    # Code for process 2
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()

# Ensure ADB connection is established first
def setup_adb():
    # Restart ADB server and connect over Wi-Fi
    subprocess.call([r'device.bat'])  # Assuming device.bat is your setup script
    time.sleep(5)  # Wait for the ADB connection to establish

# Start both processes
if __name__ == '__main__':
    # First, setup ADB connection
    setup_adb()

    # Wait for device to connect before starting processes
    while True:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if "device" in result.stdout:
            print("Device is connected.")
            break
        else:
            print("Waiting for device to connect...")
            time.sleep(2)

    # After ensuring the device is connected, start processes
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)

    p1.start()
    p2.start()

    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stop")
