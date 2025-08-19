import glob

# Find all failed chunk files
failed_files = glob.glob("failed_chunk_*.txt")

all_failed_urls = []

for file in failed_files:
    with open(file, "r") as f:
        urls = f.read().splitlines()
        all_failed_urls.extend(urls)

# Remove duplicates (optional)
all_failed_urls = list(set(all_failed_urls))

# Save merged failed URLs
with open("merged_failed_urls.txt", "w") as f:
    for url in all_failed_urls:
        f.write(url + "\n")

print(f"✅ Merged {len(failed_files)} files with {len(all_failed_urls)} unique failed URLs into merged_failed_urls.txt")
