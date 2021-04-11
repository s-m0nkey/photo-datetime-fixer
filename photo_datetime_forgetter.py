import sys
import time
import glob
from exif_manager import ExifManager

"""
## Usage
python3 photo_datetime_forgetter.py <dir> <fix/restore_id>
"""

print("+--------------------------------+")
print("| Photo Fix or Restore Forgetter |")
print("+--------------------------------+")

target_dir = sys.argv[1]
fix_restore_id = sys.argv[2]
files = glob.glob(target_dir + "/*")    # 対象ファイルリスト
files.sort()

print("Target Dir: " + target_dir)
print("Fix/Restore ID: " + fix_restore_id)
print()

for file in files:
    print(file.split("/")[-1] + ": ", end='')   # 対象ファイル
    exif_mamager = ExifManager(file)

    for comments in exif_mamager.user_comment.split("edDateTimeOriginal_"):
        if comments.split("[")[0] == fix_restore_id:
            # コメントをforget
            print("Forget.")
            print("    " + exif_mamager.user_comment)
            print(" -> " + exif_mamager.forget_exif(fix_restore_id))
            break
    else:
        print("Skip.")

print()
print("+---------------+")
print("| 🍻Forgotten🍻 |")
print("+---------------+")
