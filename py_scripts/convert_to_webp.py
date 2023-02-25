#! /usr/bin/python
import os
import sys

PROGRAM_NAME_cwebp = 'cwebp'
PROGRAM_NAME_gif2webp = 'gif2webp'

# This dict ensures we don't even attempt to process files whose extensions are not in here.
# We certainly could attempt to do that, but then the output would be cluttered with cwebp errors.
# Also, webp is mapped to None so we don't try to re-process the webp files that this script generates.
extensionMap = {
    '.png': PROGRAM_NAME_cwebp,
    '.jpeg': PROGRAM_NAME_cwebp,
    '.jpg': PROGRAM_NAME_cwebp,
    '.jpe': PROGRAM_NAME_cwebp,
    '.jif': PROGRAM_NAME_cwebp,
    '.jfif': PROGRAM_NAME_cwebp,
    '.jfi': PROGRAM_NAME_cwebp,
    '.jp2': PROGRAM_NAME_cwebp,
    '.j2k': PROGRAM_NAME_cwebp,
    '.jpf': PROGRAM_NAME_cwebp,
    '.jpx': PROGRAM_NAME_cwebp,
    '.jpm': PROGRAM_NAME_cwebp,
    '.mj2': PROGRAM_NAME_cwebp,
    '.tiff': PROGRAM_NAME_cwebp,
    '.gif': PROGRAM_NAME_gif2webp,
    '.GIF': PROGRAM_NAME_gif2webp,
    '.webp': None
}

def main():
    if len(sys.argv) == 1:
        print("webp: No target directory provided. Exiting.")
        sys.exit(1)

    # Any valid options that cwebp accepts; if invalid options are provided, the tool will complain anyway
    options = str.join(' ', sys.argv[1:-1])

    # Assume the user is competent and provides this
    target_dir = sys.argv[-1]

    # Walk the directory and any nested directories
    for dir_name, subdir_list, file_list in os.walk(target_dir):
        for file in file_list:
            img_base, ext = os.path.splitext(file)
            ext = ext.lower()

            # To prevent a key error, we have to check if ext is in the map
            conversion_tool = extensionMap[ext] if ext in extensionMap else None

            # conversion_tool may be None if the file's extension is 'webp', for example, since we don't
            # want to reprocess files we've generated ourselves
            if not conversion_tool:
                continue
            
            img_path_no_ext = os.path.join(dir_name, img_base)

            # Convert the file to webp
            os.system(f"{conversion_tool} {options} {img_path_no_ext}{ext} -o {img_path_no_ext}.webp")
            print('\n')

            # Remove the file
            os.remove(os.path.join(dir_name, file))

            
            

if __name__ == "__main__":
    main()