# Інструкція з публікації на GitHub

## Крок 1: Створення репозиторію на GitHub

1. Перейдіть на [GitHub](https://github.com)
2. Натисніть кнопку **"New"** або **"+"** → **"New repository"**
3. Заповніть форму:
   - **Repository name**: `secure-file-deleter`
   - **Description**: `Desktop application for secure file deletion using German VSITR algorithm (7-pass overwrite)`
   - **Public** або **Private** (на ваш вибір)
   - ❌ НЕ ставте галочку "Initialize this repository with a README"
   - ❌ НЕ додавайте .gitignore (вже є)
   - ❌ НЕ додавайте license (вже є)
4. Натисніть **"Create repository"**

## Крок 2: Ініціалізація Git локально

Відкрийте термінал у папці проєкту (`c:/Users/www/Desktop/Hz/Lb5`) та виконайте:

```bash
# Ініціалізація Git репозиторію
git init

# Додавання всіх файлів
git add .

# Перший commit
git commit -m "Initial commit: Secure File Deleter with German VSITR algorithm"
```

## Крок 3: Підключення до GitHub

Замініть `YOUR_USERNAME` на ваше ім'я користувача GitHub:

```bash
# Додавання віддаленого репозиторію
git remote add origin https://github.com/YOUR_USERNAME/secure-file-deleter.git

# Перейменування гілки на main (якщо потрібно)
git branch -M main

# Відправка коду на GitHub
git push -u origin main
```

## Крок 4: Налаштування репозиторію на GitHub

### 4.1. Додавання Topics (теги)

На сторінці репозиторію натисніть ⚙️ біля "About" та додайте topics:
- `python`
- `tkinter`
- `file-deletion`
- `data-security`
- `german-vsitr`
- `secure-delete`
- `data-sanitization`
- `desktop-application`

### 4.2. Додавання опису

У полі "Description" вставте:
```
🔒 Desktop application for secure file deletion using German VSITR algorithm (7-pass overwrite). Supports read-only files, includes GUI, progress tracking, and detailed logging.
```

### 4.3. Додавання Website (опціонально)

Якщо маєте GitHub Pages або документацію онлайн, додайте посилання.

## Крок 5: Створення Release (опціонально)

1. Перейдіть на вкладку **"Releases"**
2. Натисніть **"Create a new release"**
3. Заповніть:
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**:
     ```markdown
     ## 🎉 Initial Release
     
     ### Features
     - ✅ German VSITR algorithm (7-pass overwrite)
     - ✅ Graphical user interface (tkinter)
     - ✅ Support for read-only files
     - ✅ Progress tracking
     - ✅ Detailed logging
     - ✅ File renaming (3 times)
     - ✅ Comprehensive documentation
     
     ### Installation
     ```bash
     pip install -r requirements.txt
     python secure_file_deleter.py
     ```
     
     ### Documentation
     - [README.md](README.md) - Main documentation
     - [QUICK_START.md](QUICK_START.md) - Quick start guide
     - [USAGE_GUIDE.md](USAGE_GUIDE.md) - User manual
     - [EXPERIMENTS.md](EXPERIMENTS.md) - Experiment instructions
     ```
4. Натисніть **"Publish release"**

## Крок 6: Додавання README badges (опціонально)

Додайте на початок README.md:

```markdown
# Secure File Deleter

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

## Крок 7: Структура репозиторію

Після публікації ваш репозиторій матиме таку структуру:

```
secure-file-deleter/
├── .gitignore                  # Git ignore файл
├── LICENSE                     # MIT ліцензія
├── README.md                   # Основна документація
├── CONTRIBUTING.md             # Інструкції для контрибуторів
├── COMPLIANCE_CHECK.md         # Звіт про відповідність
├── EXPERIMENTS.md              # Інструкції експериментів
├── USAGE_GUIDE.md              # Посібник користувача
├── QUICK_START.md              # Швидкий старт
├── REPORT_TEMPLATE.md          # Шаблон звіту
├── requirements.txt            # Залежності Python
├── secure_file_deleter.py      # Основна програма
└── create_test_files.py        # Генератор тестових файлів
```

## Крок 8: Подальша робота з Git

### Додавання змін

```bash
# Перегляд статусу
git status

# Додавання змінених файлів
git add .

# Commit змін
git commit -m "Опис змін"

# Відправка на GitHub
git push
```

### Створення нової гілки

```bash
# Створення та перехід на нову гілку
git checkout -b feature/new-feature

# Робота над змінами...

# Commit та push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### Оновлення з GitHub

```bash
# Отримання останніх змін
git pull origin main
```

## Крок 9: Налаштування GitHub Actions (опціонально)

Створіть файл `.github/workflows/python-app.yml` для автоматичного тестування:

```yaml
name: Python Application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Test import
      run: python -c "import secure_file_deleter"
```

## Крок 10: Додавання скріншотів (рекомендовано)

1. Створіть папку `screenshots/` у репозиторії
2. Додайте скріншоти програми
3. Оновіть README.md з посиланнями на скріншоти:

```markdown
## Screenshots

![Main Window](screenshots/main_window.png)
![File Selection](screenshots/file_selection.png)
![Progress](screenshots/progress.png)
```

## Корисні команди Git

```bash
# Перегляд історії
git log --oneline

# Перегляд змін
git diff

# Скасування змін
git checkout -- filename

# Видалення файлу з Git
git rm filename

# Перейменування файлу
git mv oldname newname

# Перегляд віддалених репозиторіїв
git remote -v

# Клонування репозиторію
git clone https://github.com/YOUR_USERNAME/secure-file-deleter.git
```

## Поширені проблеми

### Помилка: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/secure-file-deleter.git
```

### Помилка: "failed to push some refs"

```bash
git pull origin main --rebase
git push origin main
```

### Великі файли

Якщо файли більше 100 MB, використовуйте Git LFS:

```bash
git lfs install
git lfs track "*.png"
git add .gitattributes
```

## Підтримка

Якщо виникли проблеми:
1. Перевірте [GitHub Docs](https://docs.github.com)
2. Створіть Issue у репозиторії
3. Зверніться до спільноти GitHub

---

**Готово!** Ваш проєкт тепер на GitHub! 🎉

Не забудьте:
- ⭐ Поставити зірку своєму репозиторію
- 📝 Оновлювати документацію
- 🐛 Виправляти баги
- ✨ Додавати нові функції