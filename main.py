import json
import os
import platform

def clear_screen():
    """清除螢幕"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def safe_input(prompt):
    print("(可隨時輸入 00 取消操作)")
    value = input(prompt)
    if value == "00":
        raise KeyboardInterrupt  # 利用例外中斷流程
    return value

class JsonDataManager:
    """管理 JSON 檔案的新增、讀取與寫入"""
    
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class OptionSelector:
    """提供選單輸入與轉換功能"""
    
    def __init__(self, title, options):
        self.title = title
        self.options = options

    def get_selection(self):
        print(f"\n=== {self.title} ===")
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")
        print("00. 取消操作並返回主選單")

        while True:
            try:
                choice = input("請選擇數字: ")
                if choice == "00":
                    raise KeyboardInterrupt
                choice = int(choice)
                if 1 <= choice <= len(self.options):
                    return self.options[choice - 1]
                else:
                    print("❌ 請輸入正確的選項號碼。")
            except ValueError:
                print("❌ 請輸入數字。")


# === 主程式 ===
def main():
    doctors_file = "doctors.json"
    schedule_file = "schedule.json"

    doctor_manager = JsonDataManager(doctors_file)
    schedule_manager = JsonDataManager(schedule_file)
    
    hospital_list = ["北榮", "振興", "聯合仁愛", "新光", "台北國泰", "汐止國泰", "台北長庚", "基隆長庚", "台安"]
    department_list = ["內科", "外科", "骨科", "小兒科", "婦產科", "皮膚科", "整形外科", "復健科"]
    date_list = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    time_list = ["早上", "下午"]
    vip_list = ["normal", "vip"]

    while True:
        try:
            print("\n=== 主選單 ===")
            print("1. 新增班表")
            print("2. 新增醫生")
            print("3. 查詢時段")
            print("4. 離開")
            option = input("請輸入功能選項: ")

            doctors_data = doctor_manager.read()
            schedule_data = schedule_manager.read()

            if option == "1":
                # 新增班表
                print("新增班表")
                if not doctors_data:
                    print("⚠️ 目前沒有醫生資料，請先新增醫生！")
                    return

                # 選醫院
                hospital = OptionSelector("醫院", list(doctors_data.keys())).get_selection()

                # 選科別
                department = OptionSelector("科別", list(doctors_data[hospital].keys())).get_selection()

                # 選醫師
                doctor = OptionSelector("醫師", doctors_data[hospital][department]).get_selection()

                # 其他欄位
                room = safe_input("請輸入診間： ")

                date = OptionSelector("日期", date_list).get_selection()
                time = OptionSelector("時段", time_list).get_selection()
                vip = OptionSelector("重點名單", vip_list).get_selection()

                # 建立班表資料
                new_schedule = {
                    "hospital": hospital,
                    "department": department,
                    "doctor": doctor,
                    "room": room,
                    "date": date,
                    "time": time,
                    "VIP": vip
                }

                # 儲存班表
                if "schedules" not in schedule_data:
                    schedule_data["schedules"] = []
                schedule_data["schedules"].append(new_schedule)
                schedule_manager.write(schedule_data)

                clear_screen()
                print("\n✅ 已新增班表：", new_schedule)

            elif option == "2":
                # 新增醫生
                print("新增醫生")

                hospital = OptionSelector("醫院", hospital_list).get_selection()
                department = OptionSelector("科別", department_list).get_selection()
                name = safe_input("請輸入醫師姓名 (包含稱謂)： ")

                if hospital not in doctors_data:
                    doctors_data[hospital] = {}
                if department not in doctors_data[hospital]:
                    doctors_data[hospital][department] = []

                clear_screen()
                if name not in doctors_data[hospital][department]:
                    doctors_data[hospital][department].append(name)
                    doctor_manager.write(doctors_data)
                    print(f"✅ 已新增 {name} 至 {hospital} 的 {department}")
                else:
                    print("⚠️ 醫師已存在")
            
            elif option == "3":
                # 查詢時段
                print("查詢值班醫師")

                date = OptionSelector("請選擇要查詢的日期", date_list).get_selection()
                time = OptionSelector("請選擇要查詢的時段", time_list).get_selection()

                if "schedules" not in schedule_data or not schedule_data["schedules"]:
                    print("⚠️ 尚無任何班表資料")
                else:
                    found = False
                    print(f"\n📅 查詢結果：{date} {time} 值班醫師\n")
                    for schedule in schedule_data["schedules"]:
                        if schedule["date"] == date and schedule["time"] == time:
                            found = True
                            print("👨‍⚕️ 醫師：", schedule["doctor"])
                            print("🏥 醫院：", schedule["hospital"])
                            print("🩺 科別：", schedule["department"])
                            print("🚪 診間：", schedule["room"])
                            print("⭐ 重點名單：", schedule["VIP"])
                            print("-" * 30)
                    if not found:
                        print("⚠️ 沒有符合條件的班表")

            elif option == "4":
                print("退出程式")
                break
            else:
                print("無效選項")

        except KeyboardInterrupt:
            clear_screen()
            print("\n⚠️ 已取消本次操作，返回主選單")
            continue

if __name__ == "__main__":
    main()
