import json
import os

filename = "main.json"

# 1️⃣ 如果檔案不存在，先建立空的 list
if not os.path.exists(filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

# 2️⃣ 讀取現有資料
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

hospital_list = ["北榮","振興","聯合仁愛","新光","台北國泰","汐止國泰","台北長庚","基隆長庚","台安"]
index = 0
for hos in hospital_list:
    index = index +1
    print(index, hos)
# 3️⃣ 使用者輸入新資料
index = int(input("請輸入醫院： "))
hospital = hospital_list[index-1]
department = input("請輸入科別： ")
room = input("請輸入診間： ")
name = input("請輸入醫師(包含稱謂)： ")
date = input("請輸入上診日期(星期一輸入 1)： ")
time = input("請輸入上診時段(早上 1, 下午 2)： ")
vip = input("請輸入是否為重點名單(是 1, 不是 2)： ")

# 4️⃣ 建立一個新的人物物件
new_person = {
    "hospital": hospital,
    "department": department,
    "Room": room, 
    "name": name,
    "date": date,
    "time": time,
    "VIP": vip,
}

# 5️⃣ 加入清單中
data.append(new_person)

# 6️⃣ 寫回 JSON 檔
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ 已新增：", new_person)