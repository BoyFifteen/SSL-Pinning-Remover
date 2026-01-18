import subprocess
import shutil
import sys
import os
import platform

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def which(bin):
    return shutil.which(bin)

def get_npm():
    return "npm.cmd" if platform.system().lower() == "windows" else "npm"

def get_apk_mitm():
    return "apk-mitm.cmd" if platform.system().lower() == "windows" else "apk-mitm"

def ensure_environment():
    if not which("node"):
        print("Node.js not found: https://nodejs.org/")
        sys.exit(1)

    if not which("java"):
        print("Java not found: https://jdk.java.net/")
        sys.exit(1)

    npm = get_npm()
    if not which(npm):
        print("npm not found (PATH issue)")
        sys.exit(1)

    apk_mitm = get_apk_mitm()
    if not which(apk_mitm):
        print("[*] apk-mitm not found, installing...")
        r = run([npm, "install", "-g", "apk-mitm"])
        if r.returncode != 0:
            print("Failed to install apk-mitm")
            print(r.stderr)
            sys.exit(1)

def remove_ssl_pinning(apk_path, output_dir):
    if not os.path.isfile(apk_path):
        print("APK file does not exist")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    apk_mitm = get_apk_mitm()
    print("[*] Removing SSL Pinning...")

    r = run([apk_mitm, apk_path, "-o", output_dir])

    if r.returncode == 0:
        print("[✓] Done")
        print(f"[✓] Output directory: {output_dir}")
    else:
        print("[!] apk-mitm failed")
        print(r.stderr)
        sys.exit(1)

def main():
    ensure_environment()

    apk = input("APK path: ").strip().strip('"')
    out = input("Output directory (folder): ").strip().strip('"')

    remove_ssl_pinning(apk, out)

if __name__ == "__main__":
    main()
