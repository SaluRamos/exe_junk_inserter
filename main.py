import os
import sys
import shutil

def add_junk_data(file_path, mb_to_add, use_random=False):
    total_bytes = int(mb_to_add * 1024 * 1024)
    chunk_size = 1024 * 1024
    print(f"Adding {mb_to_add} MB to file...")
    try:
        with open(file_path, "ab") as f:
            writen_bytes = 0
            while writen_bytes < total_bytes:
                remaining = total_bytes - writen_bytes
                actual_size = min(remaining, chunk_size)
                if use_random:
                    data = os.urandom(actual_size)
                else:
                    data = b'\x00' * actual_size
                f.write(data)
                writen_bytes += actual_size
                print(f"Progress: {int((writen_bytes/total_bytes)*100)}%", end='\r')
        print(f"\nSuccess!")
    except PermissionError:
        print("\nPermission denied.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    original_path = sys.argv[1]
    mbytes = float(sys.argv[2])
    randomize = bool(int(sys.argv[3]))
    
    copy_path = os.path.basename(original_path)

    try:
        shutil.copy(original_path, copy_path)
    except shutil.SameFileError:
        print(f"File '{original_path}' not found.")
        exit(1)


    add_junk_data(copy_path, mbytes, randomize)