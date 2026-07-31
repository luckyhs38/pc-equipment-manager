import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3  # 변경: MS SQL Server 대신 PC 로컬 SQLite DB 사용
import os       # 변경: DB 파일을 현재 실행 파일 위치에 저장하기 위해 추가
import sys      # 변경: exe 배포 시 DB 저장 위치를 잡기 위해 추가
import pandas as pd

# =========================
# DB 연결
# =========================
# 변경: SQL Server 서버 접속 방식에서 PC에 DB 파일을 저장하는 SQLite 방식으로 변경
def get_db_path():
    # exe로 만들었을 때는 exe 파일이 있는 폴더에 DB 저장
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_dir, "person_equipment.db")


def get_db_connection():
    # 변경: pyodbc.connect() 대신 sqlite3.connect() 사용
    return sqlite3.connect(get_db_path())


def init_db():
    # 변경: SQL Server 문법(IF NOT EXISTS ... BEGIN)에서 SQLite 문법으로 변경
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PersonEquipment (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Department TEXT,
        TeamName TEXT,
        PersonName TEXT NOT NULL,
        EmployeeNo TEXT,
        PCModel TEXT,
        PCSpec TEXT,
        PCRam TEXT,
        NetworkType TEXT,
        PCYear TEXT,
        Monitor1Model TEXT,
        Monitor1Inch TEXT,
        Monitor1Year TEXT,
        Monitor2Model TEXT,
        Monitor2Inch TEXT,
        Monitor2Year TEXT,
        LaptopModel TEXT,
        LaptopSpec TEXT,
        LaptopRam TEXT,
        LaptopYear TEXT,
        ReferenceNote TEXT
    )
    """)

    # 변경: 기존 DB 파일을 재사용할 때 컬럼이 없으면 자동 추가
    required_columns = {
        "Department": "TEXT",
        "TeamName": "TEXT",
        "PersonName": "TEXT",
        "EmployeeNo": "TEXT",
        "PCModel": "TEXT",
        "PCSpec": "TEXT",
        "PCRam": "TEXT",
        "NetworkType": "TEXT",
        "PCYear": "TEXT",
        "Monitor1Model": "TEXT",
        "Monitor1Inch": "TEXT",
        "Monitor1Year": "TEXT",
        "Monitor2Model": "TEXT",
        "Monitor2Inch": "TEXT",
        "Monitor2Year": "TEXT",
        "LaptopModel": "TEXT",
        "LaptopSpec": "TEXT",
        "LaptopRam": "TEXT",
        "LaptopYear": "TEXT",
        "ReferenceNote": "TEXT"
    }

    cursor.execute("PRAGMA table_info(PersonEquipment)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE PersonEquipment ADD COLUMN {column_name} {column_type}")

    conn.commit()
    cursor.close()
    conn.close()


# 초기 테이블 생성 및 미비 컬럼 자동 보완
init_db()


# =========================
# 공통 함수
# =========================
def get_input_values():
    return {
        "Department": department_combo.get().strip(),
        "TeamName": team_entry.get().strip(),
        "PersonName": name_entry.get().strip(),
        "EmployeeNo": employee_no_entry.get().strip(),
        "PCModel": pc_model_entry.get().strip(),
        "PCSpec": pc_spec_entry.get().strip(),
        "PCRam": pc_ram_combo.get().strip(),
        "NetworkType": network_combo.get().strip(),
        "PCYear": pc_year_combo.get().strip(),
        "Monitor1Model": monitor1_entry.get().strip(),
        "Monitor1Inch": monitor1_inch_combo.get().strip(),
        "Monitor1Year": monitor1_year_combo.get().strip(),
        "Monitor2Model": monitor2_entry.get().strip(),
        "Monitor2Inch": monitor2_inch_combo.get().strip(),
        "Monitor2Year": monitor2_year_combo.get().strip(),
        "LaptopModel": laptop_model_entry.get().strip(),
        "LaptopSpec": laptop_spec_entry.get().strip(),
        "LaptopRam": laptop_ram_combo.get().strip(),
        "LaptopYear": laptop_year_combo.get().strip(),
        "ReferenceNote": reference_entry.get().strip()
    }


def clear_inputs():
    department_combo.delete(0, tk.END)  # 변경: 부서 직접 입력 Entry 초기화
    team_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    employee_no_entry.delete(0, tk.END)

    pc_model_entry.delete(0, tk.END)
    pc_spec_entry.delete(0, tk.END)
    pc_ram_combo.set("")
    network_combo.set("")
    pc_year_combo.set("")

    monitor1_entry.delete(0, tk.END)
    monitor1_inch_combo.set("")
    monitor1_year_combo.set("")
    monitor2_entry.delete(0, tk.END)
    monitor2_inch_combo.set("")
    monitor2_year_combo.set("")

    laptop_model_entry.delete(0, tk.END)
    laptop_spec_entry.delete(0, tk.END)
    laptop_ram_combo.set("")
    laptop_year_combo.set("")

    reference_entry.delete(0, tk.END)


def refresh_all():
    load_data()
    load_pc_summary()
    load_laptop_summary()
    load_monitor_summary()


# =========================
# 추가 / 수정 / 삭제
# =========================
def add_data():
    try:
        data = get_input_values()
        if not data["PersonName"]:
            messagebox.showerror("입력 오류", "이름은 필수 항목입니다.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO PersonEquipment (
            Department, TeamName, PersonName, EmployeeNo,
            PCModel, PCSpec, PCRam, NetworkType, PCYear,
            Monitor1Model, Monitor1Inch, Monitor1Year, Monitor2Model, Monitor2Inch, Monitor2Year,
            LaptopModel, LaptopSpec, LaptopRam, LaptopYear, ReferenceNote
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        cursor.close()
        conn.close()

        #messagebox.showinfo("성공", "데이터가 로컬 DB에 추가되었습니다.")  # 변경: MS SQL 문구를 로컬 DB 문구로 변경
        clear_inputs()
        refresh_all()
    except Exception as e:
        messagebox.showerror("오류", f"데이터 추가 중 오류 발생: {e}")


def update_data():
    try:
        selected_item = main_tree.focus()
        if not selected_item:
            messagebox.showerror("선택 오류", "수정할 데이터를 목록에서 먼저 선택하세요.")
            return

        item_id = main_tree.item(selected_item)["values"][0]
        data = get_input_values()
        if not data["PersonName"]:
            messagebox.showerror("입력 오류", "이름은 필수 항목입니다.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE PersonEquipment SET 
            Department=?, TeamName=?, PersonName=?, EmployeeNo=?,
            PCModel=?, PCSpec=?, PCRam=?, NetworkType=?, PCYear=?,
            Monitor1Model=?, Monitor1Inch=?, Monitor1Year=?, Monitor2Model=?, Monitor2Inch=?, Monitor2Year=?,
            LaptopModel=?, LaptopSpec=?, LaptopRam=?, LaptopYear=?, ReferenceNote=?
        WHERE ID=?
        """
        cursor.execute(query, tuple(data.values()) + (item_id,))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("성공", "데이터가 수정되었습니다.")
        clear_inputs()
        refresh_all()
    except Exception as e:
        messagebox.showerror("오류", f"데이터 수정 중 오류 발생: {e}")


def delete_data():
    try:
        selected_item = main_tree.focus()
        if not selected_item:
            messagebox.showerror("선택 오류", "삭제할 데이터를 선택하세요.")
            return

        item_id = main_tree.item(selected_item)["values"][0]
        answer = messagebox.askyesno("삭제 확인", "선택한 데이터를 삭제하시겠습니까?")
        if not answer: return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PersonEquipment WHERE ID = ?", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("성공", "데이터가 삭제되었습니다.")
        clear_inputs()
        refresh_all()
    except Exception as e:
        messagebox.showerror("오류", f"데이터 삭제 중 오류 발생: {e}")


# =========================
# 전체 목록 조회
# =========================
def load_data():
    try:
        for row in main_tree.get_children():
            main_tree.delete(row)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT ID, Department, TeamName, PersonName, EmployeeNo,
               PCModel, PCSpec, PCRam, NetworkType, PCYear,
               Monitor1Model, Monitor1Inch, Monitor1Year, Monitor2Model, Monitor2Inch, Monitor2Year,
               LaptopModel, LaptopSpec, LaptopRam, LaptopYear, ReferenceNote
        FROM PersonEquipment ORDER BY Department, TeamName, PersonName
        """)
        for row in cursor.fetchall():
            main_tree.insert("", tk.END, values=list(row))
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"데이터 로드 오류: {e}")


def fill_inputs_from_selected(event):
    selected_item = main_tree.focus()
    if not selected_item: return
    values = main_tree.item(selected_item)["values"]
    clear_inputs()

    department_combo.insert(0, values[1])  # 변경: 선택한 부서를 직접 입력 Entry에 표시
    team_entry.insert(0, values[2])
    name_entry.insert(0, values[3])
    employee_no_entry.insert(0, values[4])
    pc_model_entry.insert(0, values[5])
    pc_spec_entry.insert(0, values[6])
    pc_ram_combo.set(values[7])
    network_combo.set(values[8])
    pc_year_combo.set(values[9])
    monitor1_entry.insert(0, values[10])
    monitor1_inch_combo.set(values[11])
    monitor1_year_combo.set(values[12])
    monitor2_entry.insert(0, values[13])
    monitor2_inch_combo.set(values[14])
    monitor2_year_combo.set(values[15])
    laptop_model_entry.insert(0, values[16])
    laptop_spec_entry.insert(0, values[17])
    laptop_ram_combo.set(values[18])
    laptop_year_combo.set(values[19])
    reference_entry.insert(0, values[20])


# =========================
# 현황 요약 조회
# =========================
def load_pc_summary():
    try:
        for row in pc_summary_tree.get_children(): pc_summary_tree.delete(row)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT PCModel, COUNT(*) FROM PersonEquipment WHERE PCModel IS NOT NULL AND LTRIM(RTRIM(PCModel)) <> '' GROUP BY PCModel ORDER BY COUNT(*) DESC, PCModel")
        for row in cursor.fetchall(): pc_summary_tree.insert("", tk.END, values=list(row))
        cursor.close(); conn.close()
    except: pass

def load_laptop_summary():
    try:
        for row in laptop_summary_tree.get_children(): laptop_summary_tree.delete(row)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT LaptopModel, COUNT(*) FROM PersonEquipment WHERE LaptopModel IS NOT NULL AND LTRIM(RTRIM(LaptopModel)) <> '' GROUP BY LaptopModel ORDER BY COUNT(*) DESC, LaptopModel")
        for row in cursor.fetchall(): laptop_summary_tree.insert("", tk.END, values=list(row))
        cursor.close(); conn.close()
    except: pass

def load_monitor_summary():
    try:
        for row in monitor_summary_tree.get_children(): monitor_summary_tree.delete(row)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT ModelName, COUNT(*) FROM (
            SELECT Monitor1Model AS ModelName FROM PersonEquipment WHERE Monitor1Model IS NOT NULL AND LTRIM(RTRIM(Monitor1Model)) <> ''
            UNION ALL
            SELECT Monitor2Model AS ModelName FROM PersonEquipment WHERE Monitor2Model IS NOT NULL AND LTRIM(RTRIM(Monitor2Model)) <> ''
        ) A GROUP BY ModelName ORDER BY COUNT(*) DESC, ModelName
        """)
        for row in cursor.fetchall(): monitor_summary_tree.insert("", tk.END, values=list(row))
        cursor.close(); conn.close()
    except: pass


# =========================
# 모델 현황 클릭 액션
# =========================
def select_pc_model(event):
    selected_item = pc_summary_tree.focus()
    if not selected_item: return
    pc_model_entry.delete(0, tk.END)
    pc_model_entry.insert(0, pc_summary_tree.item(selected_item)["values"][0])

def select_laptop_model(event):
    selected_item = laptop_summary_tree.focus()
    if not selected_item: return
    laptop_model_entry.delete(0, tk.END)
    laptop_model_entry.insert(0, laptop_summary_tree.item(selected_item)["values"][0])

def select_monitor_model(event):
    selected_item = monitor_summary_tree.focus()
    if not selected_item: return
    model_name = monitor_summary_tree.item(selected_item)["values"][0]
    if monitor1_entry.get().strip() == "": monitor1_entry.insert(0, model_name)
    elif monitor2_entry.get().strip() == "": monitor2_entry.insert(0, model_name)
    else: monitor1_entry.delete(0, tk.END); monitor1_entry.insert(0, model_name)


# =========================
# Excel 및 검색
# =========================
def export_to_excel():
    try:
        conn = get_db_connection()
        query = "SELECT Department AS 부서, TeamName AS 팀, PersonName AS 이름, EmployeeNo AS 사번, PCModel AS 'PC(모델)', PCSpec AS 'PC(사양)', PCRam AS 'PC(램)', NetworkType AS '내/외부망', PCYear AS 'PC(연식)', Monitor1Model AS 모니터1, Monitor1Inch AS '모니터1(인치)', Monitor1Year AS '모니터1(연식)', Monitor2Model AS 모니터2, Monitor2Inch AS '모니터2(인치)', Monitor2Year AS '모니터2(연식)', LaptopModel AS '노트북(모델)', LaptopSpec AS '노트북(사양)', LaptopRam AS '노트북(램)', LaptopYear AS '노트북(연식)', ReferenceNote AS 참고 FROM PersonEquipment ORDER BY Department, TeamName, PersonName"
        df = pd.read_sql(query, conn)
        df.to_excel("person_equipment_v3.xlsx", index=False)  # 변경: 기존 Excel 저장 파일명 유지
        conn.close()
        messagebox.showinfo("성공", "Excel 파일로 저장되었습니다.\n\nperson_equipment_v3.xlsx")  # 변경: 기존 Excel 저장 파일명 유지
    except Exception as e:
        messagebox.showerror("오류", f"Excel 저장 중 오류 발생: {e}")

def search_data():
    keyword = f"%{search_entry.get().strip()}%"
    for row in main_tree.get_children(): main_tree.delete(row)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT ID, Department, TeamName, PersonName, EmployeeNo, PCModel, PCSpec, PCRam, NetworkType, PCYear, Monitor1Model, Monitor1Inch, Monitor1Year, Monitor2Model, Monitor2Inch, Monitor2Year, LaptopModel, LaptopSpec, LaptopRam, LaptopYear, ReferenceNote FROM PersonEquipment WHERE Department LIKE ? OR TeamName LIKE ? OR PersonName LIKE ? OR EmployeeNo LIKE ? OR PCModel LIKE ? OR PCSpec LIKE ? OR ReferenceNote LIKE ? ORDER BY Department, TeamName, PersonName"
        cursor.execute(query, (keyword, keyword, keyword, keyword, keyword, keyword, keyword))
        for row in cursor.fetchall(): main_tree.insert("", tk.END, values=list(row))
        cursor.close(); conn.close()
    except Exception as e: print(e)

def reset_search():
    search_entry.delete(0, tk.END)
    load_data()


# =========================
# UI - 레이아웃 빌드
# =========================
app = tk.Tk()
app.title("사람별 장비 관리 대장 (SQLite 로컬 DB)")  # 변경: MS SQL 문구를 SQLite 로컬 DB 문구로 변경
app.geometry("1600x900")
app.state("zoomed")

COLOR_BG = "#EEF5FF"; COLOR_CARD = "#FFFFFF"; COLOR_PRIMARY = "#1E5AA8"; COLOR_PRIMARY_DARK = "#174A8B"; COLOR_BORDER = "#B7CBE8"; COLOR_TEXT = "#1F2937"; COLOR_TABLE_HEADER = "#DCEBFF"; COLOR_SELECTED = "#BBD7FF"
app.configure(bg=COLOR_BG)
style = ttk.Style(); style.theme_use("clam")
style.configure("Treeview", background="white", foreground=COLOR_TEXT, rowheight=28, fieldbackground="white", bordercolor=COLOR_BORDER, borderwidth=1, font=("맑은 고딕", 9))
style.configure("Treeview.Heading", background=COLOR_TABLE_HEADER, foreground=COLOR_PRIMARY_DARK, font=("맑은 고딕", 9, "bold"), relief="flat")
style.map("Treeview", background=[("selected", COLOR_SELECTED)], foreground=[("selected", "black")])

def make_card(parent, title): return tk.LabelFrame(parent, text=title, bg=COLOR_CARD, fg=COLOR_PRIMARY_DARK, font=("맑은 고딕", 10, "bold"), bd=1, relief="solid", padx=10, pady=5)
def make_label(parent, text, row, col): label = tk.Label(parent, text=text, bg=COLOR_CARD, fg=COLOR_TEXT, font=("맑은 고딕", 9)); label.grid(row=row, column=col, padx=4, pady=4, sticky="w"); return label
def make_entry(parent, row, col, width=20): entry = tk.Entry(parent, width=width, relief="solid", bd=1, font=("맑은 고딕", 9), highlightthickness=1, highlightbackground=COLOR_BORDER, highlightcolor=COLOR_PRIMARY); entry.grid(row=row, column=col, padx=4, pady=4); return entry
def make_combo(parent, row, col, values, width=18): combo = ttk.Combobox(parent, values=values, width=width, font=("맑은 고딕", 9)); combo.grid(row=row, column=col, padx=4, pady=4); return combo
def make_blue_button(parent, text, command, width=12): btn = tk.Button(parent, text=text, command=command, width=width, bg=COLOR_PRIMARY, fg="white", activebackground=COLOR_PRIMARY_DARK, activeforeground="white", relief="flat", font=("맑은 고딕", 9, "bold"), cursor="hand2"); btn.pack(side="left", padx=5, pady=5); return btn
def make_gray_button(parent, text, command, width=12): btn = tk.Button(parent, text=text, command=command, width=width, bg="#E5E7EB", fg=COLOR_TEXT, activebackground="#D1D5DB", activeforeground=COLOR_TEXT, relief="flat", font=("맑은 고딕", 9), cursor="hand2"); btn.pack(side="left", padx=5, pady=5); return btn

header_frame = tk.Frame(app, bg=COLOR_PRIMARY, height=60)
header_frame.pack(fill="x")
tk.Label(header_frame, text="사람별 장비 관리 대장", bg=COLOR_PRIMARY, fg="white", font=("맑은 고딕", 18, "bold")).pack(side="left", padx=25, pady=14)

main_frame = tk.Frame(app, bg=COLOR_BG)
main_frame.pack(fill="both", expand=True, padx=12, pady=12)

right_frame = tk.Frame(main_frame, bg=COLOR_BG, width=200)
right_frame.pack(side="right", fill="y", padx=(10, 0)); right_frame.pack_propagate(False)

left_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_frame.pack(side="left", fill="both", expand=True)

input_container = tk.Frame(left_frame, bg=COLOR_BG)
input_container.pack(fill="x", padx=5, pady=5)
input_container.grid_columnconfigure((0,1,2,3), weight=1)

YEAR_LIST = ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]

# 1. 기본 정보 카드
basic_frame = make_card(input_container, "기본 정보"); basic_frame.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")
make_label(basic_frame, "부서", 0, 0)
department_combo = make_entry(basic_frame, 0, 1, width=18)  # 변경: 부서를 선택 방식에서 직접 입력 방식으로 변경
make_label(basic_frame, "팀", 1, 0); team_entry = make_entry(basic_frame, 1, 1, width=18)
make_label(basic_frame, "이름", 2, 0); name_entry = make_entry(basic_frame, 2, 1, width=18)
make_label(basic_frame, "사번", 3, 0); employee_no_entry = make_entry(basic_frame, 3, 1, width=18)
make_label(basic_frame, "참고", 4, 0); reference_entry = make_entry(basic_frame, 4, 1, width=18)

# 2. PC 카드
pc_frame = make_card(input_container, "PC"); pc_frame.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")
make_label(pc_frame, "PC(모델)", 0, 0); pc_model_entry = make_entry(pc_frame, 0, 1, width=22)
make_label(pc_frame, "PC(사양)", 1, 0); pc_spec_entry = make_entry(pc_frame, 1, 1, width=22)
make_label(pc_frame, "PC(램)", 2, 0); pc_ram_combo = make_combo(pc_frame, 2, 1, ["4GB", "8GB", "16GB", "32GB", "64GB"], width=19)
make_label(pc_frame, "내/외부망", 3, 0); network_combo = make_combo(pc_frame, 3, 1, ["내부망", "외부망", "내/외부망"], width=19)
make_label(pc_frame, "PC(연식)", 4, 0); pc_year_combo = make_combo(pc_frame, 4, 1, YEAR_LIST, width=19)

# 3. 모니터 카드
monitor_frame = make_card(input_container, "모니터"); monitor_frame.grid(row=0, column=2, padx=6, pady=6, sticky="nsew")
make_label(monitor_frame, "모니터1", 0, 0); monitor1_entry = make_entry(monitor_frame, 0, 1, width=22)
make_label(monitor_frame, "모니터1(인치)", 1, 0); monitor1_inch_combo = make_combo(monitor_frame, 1, 1, ["22", "24", "27", "32", "34"], width=19)
make_label(monitor_frame, "모니터1(연식)", 2, 0); monitor1_year_combo = make_combo(monitor_frame, 2, 1, YEAR_LIST, width=19)
make_label(monitor_frame, "모니터2", 3, 0); monitor2_entry = make_entry(monitor_frame, 3, 1, width=22)
make_label(monitor_frame, "모니터2(인치)", 4, 0); monitor2_inch_combo = make_combo(monitor_frame, 4, 1, ["22", "24", "27", "32", "34"], width=19)
make_label(monitor_frame, "모니터2(연식)", 5, 0); monitor2_year_combo = make_combo(monitor_frame, 5, 1, YEAR_LIST, width=19)

# 4. 노트북 카드
laptop_frame = make_card(input_container, "노트북"); laptop_frame.grid(row=0, column=3, padx=6, pady=6, sticky="nsew")
make_label(laptop_frame, "노트북(모델)", 0, 0); laptop_model_entry = make_entry(laptop_frame, 0, 1, width=22)
make_label(laptop_frame, "노트북(사양)", 1, 0); laptop_spec_entry = make_entry(laptop_frame, 1, 1, width=22)
make_label(laptop_frame, "노트북(램)", 2, 0); laptop_ram_combo = make_combo(laptop_frame, 2, 1, ["4GB", "8GB", "16GB", "32GB", "64GB"], width=19)
make_label(laptop_frame, "노트북(연식)", 3, 0); laptop_year_combo = make_combo(laptop_frame, 3, 1, YEAR_LIST, width=19)

button_card = tk.Frame(left_frame, bg=COLOR_BG)
button_card.pack(fill="x", padx=5, pady=5)
make_blue_button(button_card, "추가", add_data)
make_blue_button(button_card, "수정", update_data)
make_blue_button(button_card, "삭제", delete_data)
make_gray_button(button_card, "초기화", clear_inputs)
make_blue_button(button_card, "Excel 저장", export_to_excel)

search_card = make_card(left_frame, "검색"); search_card.pack(fill="x", padx=5, pady=5)
search_inner = tk.Frame(search_card, bg=COLOR_CARD); search_inner.pack(fill="x")
tk.Label(search_inner, text="검색어", bg=COLOR_CARD, fg=COLOR_TEXT, font=("맑은 고딕", 9, "bold")).pack(side="left", padx=5)
search_entry = tk.Entry(search_inner, width=45, relief="solid", bd=1, font=("맑은 고딕", 9), highlightthickness=1, highlightbackground=COLOR_BORDER, highlightcolor=COLOR_PRIMARY)
search_entry.pack(side="left", padx=5, pady=5)
make_blue_button(search_inner, "검색", search_data, width=10)
make_gray_button(search_inner, "전체보기", reset_search, width=10)

table_card = make_card(left_frame, "전체 목록"); table_card.pack(fill="both", expand=True, padx=5, pady=5)
table_card.grid_rowconfigure(0, weight=1); table_card.grid_columnconfigure(0, weight=1)

# 하단 출력 기둥 정의 
main_columns = ["ID", "부서", "팀", "이름", "사번", "PC(모델)", "PC(사양)", "PC(램)", "망구분", "PC(연식)", "모니터1", "M1(인치)", "M1(연식)", "모니터2", "M2(인치)", "M2(연식)", "노트북(모델)", "노트북(사양)", "노트북(램)", "노트북(연식)", "참고"]
main_tree = ttk.Treeview(table_card, columns=main_columns, show="headings", height=15)
main_tree.grid(row=0, column=0, sticky="nsew")
main_scroll_y = ttk.Scrollbar(table_card, orient="vertical", command=main_tree.yview); main_scroll_y.grid(row=0, column=1, sticky="ns")
main_scroll_x = ttk.Scrollbar(table_card, orient="horizontal", command=main_tree.xview); main_scroll_x.grid(row=1, column=0, sticky="ew")
main_tree.configure(yscrollcommand=main_scroll_y.set, xscrollcommand=main_scroll_x.set)

# 따옴표 한 글자 빠진 만큼 폭 최적화 재조정 완료
column_widths = {
    "ID": 25, "부서": 65, "팀": 50, "이름": 45, "사번": 50, 
    "PC모델": 60, "PC사양": 60, "PC램": 35, "망구분": 45, "PC연식": 45, 
    "모니터1": 60, "M1 인치": 45, "M1 연식": 45, 
    "모니터2": 60, "M2 인치": 45, "M2 연식": 45, 
    "노트북모델": 65, "노트북사양": 65, "노트북램": 35, "노트북연식": 50, "참고": 75
}
for col in main_columns:
    main_tree.heading(col, text=col, anchor=tk.CENTER)
    main_tree.column(col, width=column_widths.get(col, 50), minwidth=column_widths.get(col, 50), anchor=tk.CENTER)
main_tree.bind("<<TreeviewSelect>>", fill_inputs_from_selected)

# 오른쪽 현황판 설정
summary_header = tk.Frame(right_frame, bg=COLOR_PRIMARY, height=45); summary_header.pack(fill="x", pady=(0, 8))
tk.Label(summary_header, text="모델명 현황", bg=COLOR_PRIMARY, fg="white", font=("맑은 고딕", 12, "bold")).pack(pady=12)

def make_summary_box(parent, title):
    frame = make_card(parent, title); frame.pack(fill="x", padx=2, pady=5)
    tree = ttk.Treeview(frame, columns=["모델명", "수량"], show="headings", height=7)
    tree.heading("모델명", text="모델명"); tree.heading("수량", text="수량")
    tree.column("모델명", width=110)
    tree.column("수량", width=40, anchor="center")
    tree.pack(fill="x", padx=3, pady=3)
    return tree

pc_summary_tree = make_summary_box(right_frame, "PC 현황")
monitor_summary_tree = make_summary_box(right_frame, "모니터 현황")
laptop_summary_tree = make_summary_box(right_frame, "노트북 현황")
pc_summary_tree.bind("<<TreeviewSelect>>", select_pc_model)
monitor_summary_tree.bind("<<TreeviewSelect>>", select_monitor_model)
laptop_summary_tree.bind("<<TreeviewSelect>>", select_laptop_model)

refresh_all()
app.mainloop()
