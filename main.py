import subprocess
import os
import sys
def install_dependencies():
    try:
        node_check = subprocess.run(["node", "-v"], capture_output=True, text=True)
        if node_check.returncode != 0:
            print("Node.js not found. Please install it from https://nodejs.org/")
            sys.exit(1)
        print("Installing apk-mitm...")
        subprocess.run(["npm", "install", "-g", "apk-mitm"], check=True)
        print("All dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        sys.exit(1)
def patch_apk(input_apk_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        command = ["apk-mitm", input_apk_path, "-o", output_dir]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Successfully patched APK. Output saved to: {output_dir}")
        else:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

def main():
    java_check = subprocess.run(["java", "-version"], capture_output=True, text=True)
    if java_check.returncode != 0:
        print("OpenJDK not found. Please install it from https://jdk.java.net/ and try again.")
        sys.exit(1)
    install_dependencies()
    input_apk = input("Enter the path to the APK file: ").strip()
    output_directory = input("Enter the output directory path: ").strip()
    if not os.path.isfile(input_apk):
        print("The specified APK file does not exist. Please check the path and try again.")
        sys.exit(1)
    patch_apk(input_apk, output_directory)
if __name__ == "__main__":
    main()
