import requests
import os
import json
import time
import sys
import re
import random
# from tqdm import tqdm
from rich.progress import track

host = "https://portal.ctdb.hcmus.edu.vn"
cookie = ""
student_id = ""
class_prefix = ""
nocheck = False

####################
#      Utils       #
####################

def get_headers():
  return {
    "Cookie": cookie,
    "X-Official-Request": "TRUE",
    "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.{str(random.random())} Safari/537.36",
  }

def init():
  global cookie

  if not os.path.exists("cookie.txt"):
    print("File cookie.txt not found. Please try again...")
    return False

  cookie = open("cookie.txt", "r").read().strip()

s = requests.Session()
# s.get(host, headers=get_headers())

####################
#    loot_dkhp     #
####################

def get_courses(student_info):
  data = {
    "action": (None, "loadDangKyHocPhan"),
    "data": (None, student_id)
  }

  r = s.post(f"{host}/dang-ky-hoc-phan/sinh-vien-apcs", files=data, headers=get_headers())

  try:
    res = json.loads(r.text)

    student_info["remaining_credits"] = student_info["max_credits"]
    student_info["remaining_courses"] = student_info["max_courses"]
    for course in res["Results"]["ListDaDangKy"]:
      student_info["remaining_credits"] -= int(course["SoTinChi"])
      student_info["remaining_courses"] -= 1

    return res["Results"]["ListChuaDangKy"], student_info
  except:
    if "<html>" in r.text:
      print("Seems like cookie is outdated, please update...")
    else:
      print("Unknown error, please try again...")
    
    return []

def get_student_info():
  data = {
    "action": (None, "loadSinhVienInfo"),
    "data": (None, student_id)
  }

  r = s.post(f"{host}/dang-ky-hoc-phan/sinh-vien-apcs", files=data, headers=get_headers())
  
  try:
    res = json.loads(r.text)
    res = res["Results"]
    return {
      "id": res["MaSV"],
      "max_courses": int(res["SoMonMax"]),
      "max_credits": int(res["SoTCMax"])
    }
  except:
    if "<html>" in r.text:
      print("Seems like cookie is outdated, please update...")
    else:
      print("Unknown error, please try again...")
    
    return {
      "id": "0",
      "max_courses": 0,
      "max_credits": 0
    }

def enroll_course(course_id, id):
  data = {
    "action": (None, "addMonDangKy"),
    "data": (None, f'{{"MaSV":{str(id)},"MaMG":{str(course_id)}}}')
  }

  r = s.post(f"{host}/dang-ky-hoc-phan/sinh-vien-apcs", files=data, headers=get_headers())
  
  try:
    res = json.loads(r.text)
    return res["Results"] == "Success"
  except:
    if "<html>" in r.text:
      print("Seems like cookie is outdated, please update...")
    else:
      print("Unknown error, please try again...")
    
    return False

def loot():
  student_info = get_student_info()
  courses, student_info = get_courses(student_info)
  matched_courses = list(filter(lambda x: class_prefix in x["MaLopHP"], courses))
  chosen_courses = []
  sum_credits = 0
  for course in matched_courses:
    if len(chosen_courses) == student_info["remaining_courses"]:
      break

    if eval(course["SoSVTT"]) == 1:
      # Full
      continue

    if sum_credits + int(course["SoTinChi"]) <= student_info["remaining_credits"]:
      sum_credits += int(course["SoTinChi"])
      chosen_courses.append(course)

  print(f"{len(chosen_courses)} courses with {sum_credits} credits will be looted...")
  for course in chosen_courses:
    print(f"{course['TenTA']} - {course['SoTinChi']} credits")

  if not no_check:
    print("Enter to loot...")
    input()
  
  print("Proceeding...")

  for course in chosen_courses:
    resp = enroll_course(course["MaMG"], student_info["id"])
    print(f'{course["TenTA"]} - {"Noice" if resp else "Oops, failed"}')

  print("Done! Enjoy ;)")

def poll_status():
  data_time = {
    "action": (None, "checkThoiGianDangKy"),
    "data": (None, "")
  }
  data_courses = {
    "action": (None, "loadDangKyHocPhan"),
    "data": (None, student_id)
  }


  while True:
    r_time = s.post(f"{host}/dang-ky-hoc-phan/sinh-vien-apcs", files=data_time, headers=get_headers())
    r_courses = s.post(f"{host}/dang-ky-hoc-phan/sinh-vien-apcs", files=data_courses, headers=get_headers())
    try:
      res_time = json.loads(r_time.text)
      res_courses = json.loads(r_courses.text)
      if res_time["Results"]["Message"] == "":
        if len(res_courses["Results"]["ListChuaDangKy"]) > 0:
          return True
        else:
          print("Sth went wrong with the portal, no avail courses, trying again...")
          for i in track(range(10), description="Waiting..."):
            time.sleep(1)
      else:
        print("Not yet...")
        for i in track(range(10), description="Waiting..."):
          time.sleep(1)
    except:
      if "<html>" in res_time.text:
        print("Seems like cookie is outdated, please update...")
      else:
        print("Unknown error, please try again...")
      
      return False

def dkhp_input():
  global cookie, student_id, class_prefix, no_check

  if len(sys.argv) > 2:
    no_check = True if sys.argv[2] == 'nocheck' else False

  while True:
    print("Please input \"your\" student ID")
    student_id = input()

    if student_id == "":
      print("Empty, please try again...")
    else:
      break

  print("Type the prefix of your courses' class to choose (e.g \"19\", \"19CTT\", etc). Leave blank if loot all <(\")")
  class_prefix = input()

  return True

####################
#      score       #
####################

def strip_html_tag(s):
  return re.sub('</?.+?>', '', s)

def get_title(score):
  score = float(score)
  return "Failure sh!t:" if score < 9 else "Name:"

def score_input():
  global student_id

  while True:
    print("Please input your student ID")
    student_id = input()

    if student_id == "":
      print("Empty, please try again...")
    else:
      break

def get_score():
  data = {
    "action": (None, 'loadKetQuaHocTap'),
    "data": (None, student_id)
  }
  r = requests.post(f'{host}/sinh-vien/ket-qua-hoc-tap', files=data, headers=get_headers())

  try:
    res = json.loads(r.text)

    if res['Status'] == 'FAILED':
      print(f'Ooops, error occured: {res["Message"]}')
      return

    res = res['Results']
    # student info
    print(f'[+] {get_title(res["DiemTBData"]["DiemTB"])} {res["SinhVienInfo"][1]["Value"]}') # name
    print(f'[+] Total credits: {res["SinhVienInfo"][8]["Value"]}')
    print(f'  [+] Mandatory: {res["SinhVienInfo"][2]["Value"]}')
    print(f'  [+] Optional: {res["SinhVienInfo"][3]["Value"]}')
    print(f'  [+] Graduation (thesis, capstone, wutev): {res["SinhVienInfo"][4]["Value"]}')
    print(f'[+] Total grade: {strip_html_tag(res["SinhVienInfo"][9]["Value"])}')
    print('-' * 10)

    # Subjects by group
    for group in res["NhomHocPhan"]:
      print(f'=== Subject group: {group["TenNhomHP"]} ===')
      for sub in group["KetQuaHocPhan"]:
        print(f'[+] {sub["MaMH"]} - {sub["TenMH"]} ({str(sub["SoTinChi"])}): {str(sub["Diem"])}')

      print('')
  except:
    if "<html" in r.text:
      print("Seems like cookie is outdated, please update...")
    else:
      print("Unknown error, please try again...")



####################
#       Main       #
####################

def main():
  if (len(sys.argv) == 1):
    print("""
    Ahem...
    I said...
    READ THE MOTHERF*CKING DOCS
    <3
    """)
    exit()

  init()

  if sys.argv[1] == 'dkhp':
    if dkhp_input():
      print("Start polling for status...")
      if poll_status():
        print("Nice, let's fcking goooo")
        loot()

  elif sys.argv[1] == 'score':
    score_input()
    print("Nice, let's fcking gooooooooo")
    get_score()

  else:
    print('Errm, either the dev is too lazy for new feature or u just mistyped...')

def banner():
  print("""
 ______              __          __      __                __
|   __ \.-----.----.|  |_.---.-.|  |    |  |_.-----.-----.|  |.-----.
|    __/|  _  |   _||   _|  _  ||  |    |   _|  _  |  _  ||  ||__ --|
|___|   |_____|__|  |____|___._||__|____|____|_____|_____||__||_____|
                                  |______| by some weeb
  Open README.md for how-to-use
  """)

if __name__ == "__main__":
  banner()
  init()
  main()
