# PC 자산관리 시스템

Python Tkinter와 SQLite를 사용한 로컬 기반 PC 자산관리 프로그램입니다.  
별도 서버 없이 실행한 PC에 DB 파일을 생성하여 PC, 모니터, 노트북 자산 정보를 관리할 수 있습니다.

<img width="3832" height="2066" alt="image" src="https://github.com/user-attachments/assets/28aaa50a-ed3b-472f-be94-934710474610" />

## 주요 기능

- 사용자별 장비 정보 등록, 수정, 삭제
- 전체 자산 목록 조회
- 부서, 팀, 이름, 사번, PC 모델 기준 검색
- PC / 모니터 / 노트북 모델별 수량 조회
- Excel 파일 저장
- 로컬 SQLite DB 자동 생성
- PyInstaller를 통한 exe 배포

## 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| GUI | Tkinter, ttk |
| Database | SQLite |
| Export | pandas, openpyxl |
| Packaging | PyInstaller |

## 프로젝트 구조

```text
pc-asset-management/
├─ app.py
├─ requirements.txt
├─ README.md
└─ .gitignore
```

## 데이터 저장 방식

프로그램 실행 시 실행 파일과 같은 폴더에 SQLite DB 파일이 자동 생성됩니다.

```text
person_equipment.db
```

사용자가 입력한 자산 정보는 이 DB 파일에 저장됩니다.

새 사용자에게 배포할 때는 `person_equipment.db`를 포함하지 않고 exe 파일만 전달하면 됩니다.  
기존 데이터를 함께 전달해야 하는 경우에는 exe 파일과 `person_equipment.db` 파일을 같이 전달해야 합니다.

## 실행 방법

### 개발 환경 실행

```bash
pip install -r requirements.txt
python app.py
```

Windows에서 `py` 명령어를 사용하는 경우:

```bash
py app.py
```

## exe 생성 방법

PyInstaller를 사용하여 Windows 실행 파일을 생성합니다.

```bash
pyinstaller --onefile --windowed --name "PC자산관리시스템" app.py
```

생성된 exe 파일은 아래 경로에 만들어집니다.

```text
dist/PC자산관리시스템.exe
```

## requirements.txt

```txt
pandas
openpyxl
pyinstaller
```

SQLite는 Python 기본 내장 모듈이므로 별도 설치가 필요하지 않습니다.

## 배포 방식

소스코드는 GitHub 저장소에서 관리하고, 사용자 실행용 exe 파일은 GitHub Releases에 첨부하여 배포합니다.

### GitHub 저장소에 포함할 파일

```text
app.py
requirements.txt
README.md
.gitignore
```

### GitHub Releases에 첨부할 파일

```text
PC자산관리시스템.exe
```

## Git에 올리지 않는 파일

아래 파일들은 사용자 데이터 또는 빌드 결과물이므로 Git에 올리지 않습니다.

```text
person_equipment.db
person_equipment_v3.xlsx
build/
dist/
__pycache__/
*.spec
```

## 권장 .gitignore

```gitignore
__pycache__/
*.pyc

build/
dist/
*.spec

person_equipment.db
*.db

person_equipment_v3.xlsx
*.xlsx

.vscode/
```

## 주요 구현 내용

### 로컬 DB 저장

기존 SQL Server 방식이 아닌 SQLite를 사용하여 별도 서버 없이 데이터를 저장할 수 있도록 구현했습니다.

프로그램 실행 시 `person_equipment.db` 파일이 자동 생성되며, 자산 정보는 해당 파일에 저장됩니다.

### CRUD 기능

사용자는 화면에서 자산 정보를 입력하고 다음 작업을 수행할 수 있습니다.

- 추가
- 수정
- 삭제
- 조회
- 검색

### 모델별 현황 조회

오른쪽 현황판에서 PC, 모니터, 노트북 모델별 등록 수량을 확인할 수 있습니다.

### Excel 저장

등록된 자산 목록을 Excel 파일로 저장할 수 있습니다.

```text
person_equipment_v3.xlsx
```

## 향후 개선 사항

- 로그인 기능 추가
- 장비 반납/폐기 이력 관리
- 자산 번호 자동 생성
- Excel 가져오기 기능
- 검색 조건 세분화
- 설치 프로그램 형태로 배포

## 버전

### v1.0.0

- SQLite 로컬 DB 저장 방식 적용
- PC, 모니터, 노트북 자산 등록/수정/삭제 기능 구현
- 모델별 현황 조회 기능 구현
- Excel 저장 기능 구현
- exe 배포 구조 적용
