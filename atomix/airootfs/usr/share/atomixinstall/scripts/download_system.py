import requests
import os
import hashlib

GITHUB_API = "https://api.github.com/repos/Atomix-Linux/atomix/releases"
DOWNLOAD_PATH = "/tmp/zenkai_root"

def sha256sum(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_file(filepath, expected_hash):
    actual_hash = sha256sum(filepath)
    if actual_hash != expected_hash:
        raise ValueError(f"Hash mismatch for {filepath}!\nExpected: {expected_hash}\nActual:   {actual_hash}")
    print(f"✅ Verified {os.path.basename(filepath)}")

def download_asset(url, dest_folder):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    print(f"⬇️  Downloading {local_filename} ...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def get_release_by_channel(channel='stable'):
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    releases = response.json()

    if channel == 'stable':
        for release in releases:
            if not release['prerelease'] and not release['draft']:
                return release
    elif channel == 'unstable':
        for release in releases:
            if release['prerelease'] and not release['draft']:
                return release
    else:
        raise ValueError("Channel must be 'stable' or 'unstable'")

    raise Exception(f"No release found for channel {channel}")

def parse_sha256_file(filepath):
    checksums = {}
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            hash_part, file_part = line.strip().split(None, 1)
            file_part = file_part.strip()
            if file_part.startswith('*') or file_part.startswith(' '):
                file_part = file_part[1:].strip()
            checksums[file_part] = hash_part
    return checksums

def download_split_files(channel='stable', dest_folder=DOWNLOAD_PATH):
    os.makedirs(dest_folder, exist_ok=True)

    # Save channel info
    with open(os.path.join(dest_folder, "channel"), 'w') as f:
        f.write(channel)

    release = get_release_by_channel(channel)
    print(f"📦 Downloading release: {release['name']} (tag: {release['tag_name']})")

    # Find SHA256 file
    sha_asset = next((a for a in release['assets'] if 'sha256' in a['name']), None)
    if not sha_asset:
        raise Exception("❌ No SHA256 file found in release.")
    
    sha_path = download_asset(sha_asset['browser_download_url'], dest_folder)
    expected_hashes = parse_sha256_file(sha_path)

    # Download and verify .part.* files
    part_assets = [a for a in release['assets'] if '.part.' in a['name']]
    if not part_assets:
        print("❌ No split .part.* files found in the release.")
        return

    for asset in part_assets:
        file_path = download_asset(asset['browser_download_url'], dest_folder)
        filename = os.path.basename(file_path)
        if filename in expected_hashes:
            verify_file(file_path, expected_hashes[filename])
        else:
            print(f"⚠️ No checksum found for {filename}, skipping verification.")

    print("✅ All parts downloaded and verified.")

if __name__ == "__main__":
    import sys
    channel = sys.argv[1] if len(sys.argv) > 1 else 'stable'
    download_split_files(channel)
