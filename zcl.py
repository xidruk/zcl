import sys
import os 
import pwd
import shutil
from zcl_linux_machine_cfps import purge_linux_cfps
from zcl_darwin_machine_cfps import purge_darwin_cfps

def detect_platform()-> str:
    platform = sys.platform

    if (platform.startswith("linux")):
        return ("linux")
    elif (platform.startswith("darwin")):
        return ("darwin")
    else:
        return ("unsupported")

def get_username()-> str:
    return (pwd.getpwuid(os.getuid()).pw_name)

def format_bytes(bytes_val: int) -> str:
    mb = bytes_val / (2 ** 20)
    gb = bytes_val / (2 ** 30)
    
    if (gb >= 1):
        return (f"{gb:.2f} GB")
    else:
        return (f"{mb:.2f} MB")

def get_disk_usage(username: str, platform: str) -> dict:
    if platform == "darwin":
        home = f"/Users/{username}"
    else:
        home = f"/home/{username}"

    path = "/"
    if (os.path.exists(home)):
        path = home
    usage = shutil.disk_usage(path)
    return {
        "total": usage.total // (2 ** 30),
        "used":  usage.used  // (2 ** 30),
        "free":  usage.free  // (2 ** 30),
        "pct":   (usage.used / usage.total) * 100,
        "used_bytes": usage.used,
    }

def display_session_info(platform: str, username: str, disk: dict):
    print()
    print("-" * 40)
    print("  ZCL — ZCleaner Session Info")
    print("-" * 40)

    if platform == "linux":
        print("  Platform  :  Linux")
    else:
        print("  Platform  :  macOS (Darwin)")

    print(f"  User      :  {username}")
    print(f"  Disk Used :  {disk['used']} GB / {disk['total']} GB  ({disk['pct']:.1f}%)")
    print(f"  Free      :  {disk['free']} GB")
    print("-" * 40)
    print()

def ask_confirmation() -> bool:
    try:
        answer = str(input("  Are you sure you want to clean the cache? (y/N): ")).strip().lower()
        if (answer == "y" or answer == "yes" or len(answer) == 0):
            return (True)
        else:
            return (False)
    except (KeyboardInterrupt, EOFError, TypeError, ValueError):
        print()
        return (False)

def main():
    platform = detect_platform()

    if platform == "unsupported":
        print()
        print("  [ERROR] Unsupported system detected.")
        print("  ZCL only supports <Linux> and <macOS> (Darwin).")
        print()
        sys.exit(1)

    username = get_username()
    disk = get_disk_usage(username, platform)

    display_session_info(platform, username, disk)

    if not ask_confirmation():
        print()
        print("  Aborted. Nothing was deleted.")
        print()
        sys.exit(0)

    print()
    print("  Cleaning cache files...")
    print()

    disk_before = get_disk_usage(username, platform)

    if platform == "darwin":
        purge_darwin_cfps(username)
    else:
        purge_linux_cfps(username)

    disk_after = get_disk_usage(username, platform)

    space_freed = disk_before["used_bytes"] - disk_after["used_bytes"]

    print()
    print("  Done! Cache cleaned successfully.")
    print()
    print("-" * 40)
    print("  Cleanup Results")
    print("-" * 40)
    print(f"  Before : {disk_before['used']} GB used")
    print(f"  After  : {disk_after['used']} GB used")
    print(f"  Freed  : {format_bytes(space_freed)}")
    print("-" * 40)
    print()

if __name__ == "__main__":
    main()