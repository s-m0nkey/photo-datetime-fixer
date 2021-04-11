import sys
import time
import glob
from exif_manager import ExifManager

"""
photo_datetime_fixer
Usage: python3 photo_datetime_restorer.py <dir> <fix_id>
指定したディレクトリ内のファイルについて、
    1. photo_date_fixer で修正した DateTimeOriginal をfix_idが一致したコメントを基に元に戻す。
    2. その旨をUserCommentに追記
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
print("Fix ID: " + restore_id + "\n")

for file in files:
    print(file.split("/")[-1] + ": ", end='')   # 対象ファイル
    exif_mamager = ExifManager(file)

    for comments in exif_mamager.user_comment.split("FixedDateTimeOriginal_"):
        if comments.split("[")[0] == fix_id:
            # 元のDateTimeOriginalに修正
            print("Restore.")
            restore_info = comments.split("[")[1][:-1].replace("->", "<-")
            print("  " + restore_info)
            restore_comment = "FixedDateTimeOriginal_" + restore_id + "[" + restore_info + "]"
            exif_mamager.write_exif(comments.split("[")[1].split(" ->")[0], restore_comment)
            break
    else:
        print("Skip.")

print()
print("+-----------+")
print("| 🍻Fixed🍻 |")
print("+-----------+")