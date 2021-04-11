import os
import datetime
import subprocess

class ExifManager:
    writable = False
    target_file = ""
    date_time_original = ""     # DateTimeOriginal
    user_comment = ""           # UserComment

    # EXIF情報取得 & 書き込み可能か確認
    def __init__(self, file):
        self.target_file = file

        ret =  subprocess.run(
            "exiftool -s -s -DateTimeOriginal -UserComment " + self.target_file,
            stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True
            ).stdout.decode()[:-1]
        lines = ret.split("\n")
        for line in lines:
            tag_value = line.split(": ")
            if tag_value[0] == "DateTimeOriginal":
                self.date_time_original = tag_value[1]
            elif tag_value[0] == "UserComment":
                self.user_comment  = tag_value[1]

        support_extensions = ["360", "3G2", "3GP", "3GP2", "3GPP", "AAX", "AI", "AIT", "APNG", 
        "ARQ", "ARW", "AVIF", "CIFF", "CR2", "CR3", "CRM", "CRW", "CS1", "DCP", "DNG", "DR4", 
        "DVB", "EPS", "EPS2", "EPS3", "EPSF", "ERF", "EXIF", "EXV", "F4A", "F4B", "F4P", "F4V", 
        "FFF", "FLIF", "GIF", "GPR", "HDP", "HEIC", "HEIF", "HIF", "ICC", "ICM", "IIQ", "IND", 
        "INDD", "INDT", "INSP", "J2K", "JNG", "JP2", "JPE", "JPEG", "JPF", "JPG", "JPM", "JPX", 
        "JXL", "JXR", "LRV", "M4A", "M4B", "M4P", "M4V", "MEF", "MIE", "MNG", "MOS", "MOV", "MP4", 
        "MPO", "MQV", "MRW", "NEF", "NRW", "ORF", "ORI", "PBM", "PDF", "PEF", "PGM", "PNG", "PPM", 
        "PS", "PS2", "PS3", "PSB", "PSD", "PSDT", "QT", "RAF", "RAW", "RW2", "RWL", "SR2", "SRW", 
        "THM", "TIF", "TIFF", "VRD", "WDP", "X3F", "XMP"]
        if os.access(file, os.W_OK) and os.path.splitext(file)[1].lstrip(".").upper() in support_extensions:
            self.writable = True
    
    # DateTimeOriginal と UserComment を更新(UserComment は追記)
    def write_exif(self, new_date_time, comment):
        space = ""
        if self.user_comment:
            space = " "

        subprocess.run(
            "exiftool -overwrite_original " + 
            "-DateTimeOriginal=\"" + new_date_time + "\" " + 
            "-UserComment=\"" + self.user_comment + space + comment + "\" " + 
            self.target_file,
            stdout = subprocess.DEVNULL,stderr = subprocess.DEVNULL, shell=True
            )

    # "yyyy:mm:dd hh:mm:ss" -> 秒
    @classmethod
    def date_time_to_sec(cls, str):
        if not str:
            return 0
        tmp = str.split()
        date = tmp[0].split(":")
        time = tmp[1].split("+")[0].split(":")
        dt = datetime.datetime(
            int(date[0]), int(date[1]), int(date[2]), 
            0, 0, 0)
        dt0 = datetime.timedelta(days=366) # dt1が西暦0年にならないので苦肉の策
        dt1 = datetime.datetime(1,1,1,0,0,0)
        td = dt + dt0 - dt1
        return ((((td.days * 24) + int(time[0])) * 60) + int(time[1])) * 60 + int(time[2])

    # 秒 -> "yyyy:mm:dd hh:mm:ss"
    @classmethod
    def sec_to_date_time(cls, sec):
        dt0 = datetime.timedelta(days=366) # dt1が西暦0年にならないので苦肉の策
        dt1 = datetime.datetime(1,1,1,0,0,0)
        dt = dt1 + datetime.timedelta(days=int(sec / (24 * 60 * 60))) - dt0
        year = dt.year
        month = dt.month
        day = dt.day

        time_sec = sec % (24 * 60 * 60)
        hour = int(time_sec / (60 * 60))
        minutes = int((time_sec - hour * 60 * 60) / 60)
        seconds = int(time_sec - hour * 60 * 60 - minutes * 60)

        return str(year).zfill(4) + ":" + str(month).zfill(2) + ":" + str(day).zfill(2) + " " + str(hour).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)