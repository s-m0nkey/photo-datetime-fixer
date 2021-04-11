import sys
import time
import glob
from exif_manager import ExifManager

"""
## Usage
python3 photo_datetime_restorer.py <dir> <fix_id>
"""

print("+----------------------------+")
print("| Photo Date & Time Restorer |")
print("+----------------------------+")

target_dir = sys.argv[1]
fix_id = sys.argv[2]
restore_id = str(int(time.time()))   # コメント記録用
files = glob.glob(target_dir + "/*")    # 対象ファイルリスト
files.sort()

print("Target Dir: " + target_dir)
print("Fix ID: " + fix_id)
print("Restore ID: " + restore_id + "\n")

for file in files:
    print(file.split("/")[-1] + ": ", end='')   # 対象ファイル
    exif_mamager = ExifManager(file)

    for comments in exif_mamager.user_comment.split("FixedDateTimeOriginal_"):
        if comments.split("[")[0] == fix_id:
            # 元のDateTimeOriginalに修正
            print("Restore.")
            daytimes = comments.split("[")[1].split("]")[0].split(" -> ")
            print("  " + daytimes[1] + " -> " + daytimes[0])
            restore_comment = "RestoredDateTimeOriginal_" + restore_id + "[" + daytimes[1] + " -> " + daytimes[0] + "]"
            exif_mamager.write_exif(daytimes[0], restore_comment)
            break
    else:
        print("Skip.")

print()
print("+-------------+")
print("| 🍻Restored🍻 |")
print("+-------------+")