import glob

# Find all failed chunk files
failed_files = glob.glob("failed_chunk_*.txt") # This will match files like failed_chunk_01.txt, failed_chunk_02.txt, etc.
# Save company links to a file

all_failed_urls = []

for file in failed_files: # Loop through each failed chunk file
    # Read the contents of the file and extend the list
    with open(file, "r") as f: # Open the file for reading
        # Read all lines and strip whitespace
        urls = f.read().splitlines() # Read all URLs from the file
        # Extend the all_failed_urls list with the URLs from the current file
        all_failed_urls.extend(urls) # Extend the list with URLs from the current file

# Remove duplicates (optional)
all_failed_urls = list(set(all_failed_urls))

# Save merged failed URLs
with open("merged_failed_urls.txt", "w") as f:
    for url in all_failed_urls:
        f.write(url + "\n")

print(f"Merged {len(failed_files)} files with {len(all_failed_urls)} unique failed URLs into merged_failed_urls.txt")
