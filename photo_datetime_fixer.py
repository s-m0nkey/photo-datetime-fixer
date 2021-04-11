import sys
import time
import glob
from exif_manager import ExifManager

"""
## Usage
python3 photo_datetime_fixer.py <dir>
"""

print("+-------------------------+")
print("| Photo Date & Time Fixer |")
print("+-------------------------+")



# exif情報の修正を行う関数
# ラストのファイルが対象の場合にはdate_time_afterをnullとする
def fix_DateTimeOriginal(exif_mamagers, date_time_before, date_time_after, files_to_fix, fix_id):
    if not files_to_fix:
        return 0
    print("Fix!")

    # 日付を秒数に変換
    before_sec = ExifManager.date_time_to_sec(date_time_before)
    after_sec = ExifManager.date_time_to_sec(date_time_after)

    # リストの数でbeforeとafterの間を均等に割る(小数点)
    # ラストの処理の場合は1s固定
    if after_sec == 0:
        interval = 1
    else:
        interval = (after_sec - before_sec) / (len(files_to_fix) + 1)

    i = 1
    for file in files_to_fix:
        print("  " + file.split("/")[-1] + ": ", end='')   # 対象ファイル
        if not exif_mamagers[file].writable:
            print("Skip: Not writable.")
            continue
        # 修正後日時の決定、四捨五入
        new_date_time_sec = round(before_sec + interval * i)
        i += 1
        # 修正後日時の文字列化
        new_date_time = ExifManager.sec_to_date_time(new_date_time_sec)
        # 追記コメント作成
        fix_comment = "FixedDateTimeOriginal_" + fix_id + "[" + exif_mamagers[file].date_time_original + " -> " + new_date_time + "]"
        # fix
        exif_mamagers[file].write_exif(new_date_time, fix_comment)
        print("Fixed: " + exif_mamagers[file].date_time_original + " -> " + new_date_time)

    # 要修正リストのクリア
    files_to_fix.clear()

target_dir = sys.argv[1]
fix_id = str(int(time.time()))   # 現在時刻(コメント記録用)
files_to_fix = []   # 修正が必要と思われるファイルのリスト
exif_mamagers = {}   # ファイル名とExifManagerの対応
files = glob.glob(target_dir + "/*")    # 対象ファイルリスト
files.sort()
date_time_before = ""    # 最後に発見した正しそうな日付

print("Target Dir: " + target_dir)
print("Fix ID: " + fix_id + "\n")

for file in files:
    print(file.split("/")[-1] + ": ", end='')   # 対象ファイル

    # managerの辞書登録
    # 現在のexif情報の取得と書き込み可能かの確認
    exif_mamagers[file] = ExifManager(file)

    # 1番目のファイルかどうか
    if not date_time_before:
        # before更新(SubSecDateTimeOriginalがあればそっち、なければDateTimeOriginalを)
        date_time_before = exif_mamagers[file].date_time_original
        print("Skip: No data before.")
        continue

    # 修正の要否の判断
    # DateTimeOriginal(SubSec優先)がbefore以前(空欄含む)
    date_time = exif_mamagers[file].date_time_original
    if date_time < date_time_before:
        # このファイルに対する修正が必要
        # リストに追加
        files_to_fix.append(file)
        print("Need to fix.")
    else:
        # このファイルに対する修正は不要
        print("OK.")
        # そこまでの問題があったファイルの修正
        fix_DateTimeOriginal(exif_mamagers, date_time_before, date_time, files_to_fix, fix_id)
        # before更新(SubSecDateTimeOriginalがあればそっち、なければDateTimeOriginalを)
        date_time_before = exif_mamagers[file].date_time_original

# ラストの処理
fix_DateTimeOriginal(exif_mamagers, date_time_before, "", files_to_fix, fix_id)

print()
print("+-----------+")
print("| 🍻Fixed🍻 |")
print("+-----------+")