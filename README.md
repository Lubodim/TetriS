# 🟦 Tetris — Python / Pygame Implementation

A modern, modular, and extensible **Tetris clone built with Python and Pygame**.

Проектът е структуриран в няколко файла (Board, Tetromino, Factory, Config и др.), използва наследяване и позволява лесно разширение — добавяне на нови форми, UI подобрения, пауза, прозрачен overlay, премахване на редове, скорост на падане и още.

---

## ✨ Features

- ✔️ Управление на падащи тетрис блокове  
- ✔️ Автоматично запазване на блоковете в дъното  
- ✔️ Изтриване на пълни редове + смъкване надолу  
- ✔️ Пауза с **полупрозрачен overlay** и диалог за изход (Да/Не)  
- ✔️ Конфигурация чрез отделен клас `Config`  
- ✔️ Чисто разделени модули: `board.py`, `tetromino.py`, `shape_factory.py`, `config.py`, `main.py`  
- ✔️ Лесно разширение

---

## 🧩 Requirements

```
pip install pygame
```

Проектът работи с **Python 3.10+**.

---

## ▶️ Running the Game

```
python main.py
```

---

## 📁 Project Structure

```
tetris/
│── main.py               # Главен игрови цикъл
│── board.py              # Игралната дъска
│── tetromino.py          # Базов клас за тетрис фигурите
│── shape_factory.py      # Фабрика за генериране на Tetromino форми
│── config.py             # Настройки (редове, колони, таймери и т.н.)
│── assets/               # Шрифтове, картинки (по желание)
│── README.md
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| ← → | Move left/right |
| ↑   | Rotate |
| ↓   | Soft drop |
| SPACE | Hard drop |
| ESC | Pause + диалог за изход |

---

## 🛠️ Customization

Можеш лесно да променяш:

- размера на решетката: `Config.rows`, `Config.cols`
- размера на плочките: `Config.tile_size`
- скоростта на падане
- цветовете и външния вид
- логиката за нови блокове чрез Shape Factory

---

## 📜 License — MIT

```
MIT License

Copyright (c) 2025 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## 💬 Feedback & Contribution

Ако искаш да продължим да го развиваме — добавяне на highscore, next preview, sound effects и т.н. — просто кажи!
