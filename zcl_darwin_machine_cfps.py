import os
import glob
import shutil


darwin_cache_paths = [
    # System Cache
    ".cache/*",
    "Library/Caches/*",
    
    # Docker
    "Library/Containers/com.docker.docker/Data/vms/0/data",
    
    # VS Code
    "Library/Application Support/Code/Cache/*",
    "Library/Application Support/Code/CachedData/*",
    "Library/Application Support/Code/CachedExtensionVSIXs",
    "Library/Application Support/Code/Crashpad/*",
    "Library/Application Support/Code/Crashpad/completed/*",
    "Library/Application Support/Code/User/workspaceStorage/*",
    "Library/Application Support/Code/Service Worker",
    "Library/Application Support/Code/WebStorage",
    "Library/Application Support/Code/User/*",
    
    # Cursor (Code Editor)
    "Library/Application Support/Cursor/Cache",
    "Library/Application Support/Cursor/CachedData",
    "Library/Application Support/Cursor/CachedExtensionVSIXs",
    "Library/Application Support/Cursor/Crashpad",
    "Library/Application Support/Cursor/User/workspaceStorage",
    "Library/Application Support/Cursor/Service Worker",
    "Library/Application Support/Cursor/WebStorage",
    
    # Slack
    "Library/Application Support/Slack/Cache/*",
    "Library/Application Support/Slack/Service Worker/*",
    "Library/Application Support/Slack/Service Worker/CacheStorage/*",
    
    # Discord
    "Library/Application Support/discord/Cache/*",
    "Library/Application Support/discord/Code Cache/js/*",
    "Library/Application Support/discord/Crashpad/completed/*",
    "Library/Application Support/discord/Service Worker",
    
    # Google Chrome
    "Library/Application Support/Google/Chrome/Default/Service Worker/CacheStorage/*",
    "Library/Application Support/Google/Chrome/Profile [0-9]/Service Worker/CacheStorage/*",
    "Library/Application Support/Google/Chrome/Default/Application Cache/*",
    "Library/Application Support/Google/Chrome/Profile [0-9]/Application Cache/*",
    "Library/Application Support/Google/Chrome/Crashpad/completed/*",
    "Library/Application Support/Google/Chrome/Default/Service Worker",
    "Library/Application Support/Google/Chrome/Default/File System",
    "Library/Application Support/Google/Chrome/Profile [0-9]/File System",
    
    # Brave Browser
    "Library/Application Support/BraveSoftware/Brave-Browser/Default/Service Worker/CacheStorage/*",
    "Library/Application Support/BraveSoftware/Brave-Browser/Profile [0-9]/Service Worker/CacheStorage/*",
    "Library/Application Support/BraveSoftware/Brave-Browser/Default/Application Cache/*",
    "Library/Application Support/BraveSoftware/Brave-Browser/Profile [0-9]/Application Cache/*",
    "Library/Application Support/BraveSoftware/Brave-Browser/Crashpad/completed/*",
    "Library/Application Support/BraveSoftware/Brave-Browser/Default/Service Worker",
    "Library/Application Support/BraveSoftware/Brave-Browser/Default/File System",
    "Library/Application Support/BraveSoftware/Brave-Browser/Profile [0-9]/File System",
    
    # Firefox
    "Library/Caches/Firefox/*",
    "Library/Application Support/Firefox/Profiles/*/cache2/*",
    
    # Opera
    "Library/Application Support/Opera Software/Opera Stable/Service Worker",
    
    # Vivaldi
    "Library/Application Support/Vivaldi/Default/Service Worker",
    
    # Chromium
    "Library/Application Support/Chromium/Default/File System",
    "Library/Application Support/Chromium/Profile [0-9]/File System",
    
    # Spotify
    "Library/Application Support/Spotify/PersistentCache/*",
    
    # iOS Simulator
    "Library/Developer/CoreSimulator/*",
    
    # 42 School Specific
    "Library/*.42*",
    "*.42*",
    ".zcompdump*",
    ".cocoapods.42_cache_bak*",
    
    # Other
    ".Trash/*",
    "Downloads/*",
    "Desktop/**/*/.DS_Store",
    "Desktop/Piscine Rules *.mp4",
    "Desktop/PLAY_ME.webloc",
    
    # Application Support Caches
    "Library/Application Support/Caches/*",
]

def _delete_target(path: str):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                shutil.rmtree(entry.path, ignore_errors=True)
            else:
                os.remove(entry.path)

def purge_darwin_cfps(username: str):
    home = f"/Users/{username}"
    deleted = 0
    errors = 0

    for pattern in darwin_cache_paths:
        full_pattern = os.path.join(home, pattern)
        matches = glob.glob(full_pattern, recursive=True)
        for match in matches:
            try:
                _delete_target(match)
                deleted += 1
            except Exception:
                errors += 1

    print(f"  => Deleted {deleted} item(s), {errors} error(s).")


def show_darwin_cfps(username: str):
    home = f"/Users/{username}"
    index = 0
    while index < len(darwin_cache_paths):
        print(f"  DARWIN CFP => {home}/{darwin_cache_paths[index]}")
        index += 1
