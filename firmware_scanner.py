import os
import re

# List of functions considered risky in C/C++ firmware
DANGEROUS_FUNCTIONS = [
    'gets', 'strcpy', 'strcat', 'sprintf', 'scanf', 'strncpy', 'memcpy'
]

def scan_file(filepath):
    with open(filepath, 'r', errors='ignore') as file:
        for lineno, line in enumerate(file, 1):
            for func in DANGEROUS_FUNCTIONS:
                pattern = r'\b' + re.escape(func) + r'\s*\('
                if re.search(pattern, line):
                    print(f"[!] Found '{func}' in {filepath} at line {lineno}:")
                    print(f"    {line.strip()}")

def scan_directory(root):
    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h')):
                scan_file(os.path.join(subdir, file))

if __name__ == "__main__":
    target = input("Enter the path to the firmware source folder: ").strip()
    if os.path.isdir(target):
        print(f"🔍 Scanning for dangerous functions in: {target}\n")
        scan_directory(target)
    else:
        print("❌ Invalid folder path.")

