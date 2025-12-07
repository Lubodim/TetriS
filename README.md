# 🟦 Tetris — Modern Python / Pygame Edition

A polished and modular **Tetris clone built with Python and Pygame**, featuring levels, scoring system, dynamic speed, next-piece preview, full game state management and customizable configuration.

Проектът използва изчистена архитектура с отделни модули: `Game`, `Board`, `Tetromino`, `Shape Factory`, `Sidebar`, `GameOverScreen`, което позволява лесно разширяване и поддръжка.

---

## ✨ Features

### 🎮 Основен геймплей
- Падащи тетрис фигури, генерирани от **TetroFactory**  
- Завъртане, хоризонтално и вертикално движение  
- **Hard Drop** със SPACE  
- Заключване на фигурите върху дъската  
- Разпознаване и премахване на запълнени редове  
- Автоматично смъкване на блоковете над тях  
- Game Over логика и пълно рестартиране

### 🎚️ Нива и скорост
Играчът преминава през **нива 1 → 10**, базирани на общия брой изчистени редове.

Според кода:  
- Нивото = `1 + (lines_cleared // 100)`  
- Максимално ниво: **10**  
- Падане на фигурите става **по-бързо на всяко следващо ниво** чрез:
```
fall_interval_ms = max(120, 500 - (level - 1) * 30)
```
Това означава:
- Ниво 1 → 500ms  
- Ниво 5 → 380ms  
- Ниво 10 → 230ms  
- Минимално: 120ms  

### 🏆 Система за точки
Според `calculate_score()` реалната точкова система е:

| Изчистени линии | Точки (× Level) |
|-----------------|----------------|
| 1 линия | 100 |
| 2 линии | 300 |
| 3 линии | 500 |
| 4 линии (Tetris!) | 800 |

Точките се умножават по текущото ниво.

Пример:  
На ниво 4, ако играчът направи Tetris (4 линии):  
`800 × 4 = 3200 точки`

### 📊 Sidebar (дясна лента)
Sidebar панелът показва:
- **Score**
- **Lines**
- **Level**
- **Next Piece Preview**

Има красив преглед на следващата фигура със скалиране в прозорец от 5 клетки височина.

### 💀 Game Over Screen
При загуба се показва полупрозрачен overlay и меню с бутони:
- **Нова игра**
- **Продължи**
- **Изход**

Бутоните са цветни и се управляват и с мишка, и с клавиатура:
- Enter → Restart  
- Space → Continue  
- Escape → Quit  

### ⌨️ Controls

| Key | Action |
|-----|--------|
| ← → | move piece |
| ↑ | rotate |
| ↓ | soft drop |
| SPACE | hard drop |
| ESC | open Game Over menu |

---

## 🧩 Project Structure

```
tetris/
│── main.py             # Стартира играта
│── game.py             # Главна логика на играта (цикъл, нива, точки, падаща скорост)
│── board.py            # Игрална дъска & логика за редове
│── shape_factory.py    # Генериране на случайни фигури
│── config.py           # Конфигурация и цветове
│── sidebar.py          # Дясна информационна лента
│── game_over.py        # Game Over меню с бутони
│── README.md
```

---

## ▶️ Running the Game

```
pip install pygame
python main.py
```

---

## 🛠️ Customization

### Промяна на размерите
`Config.cols`, `Config.rows`, `Config.tile_size`

### Промяна на скоростта и трудността
- Начална скорост: `fall_interval_ms` в `game.py`  
- Формула за ниво  
- Точкова система (в `calculate_score()`)

### Цветове
В `config.py → Colors` могат да се променят скиновете на фигурите и UI елементите.

### Добавяне на нови форми
Добави нов shape в `TetroFactory.SHAPES`.

---

## 📜 License — MIT

```
MIT License

Copyright (c) 2025 <Your Name>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 💬 Feedback & Contribution

Ако искаш, мога да ти:
- добавя **High Score система**  
- добавя **анимации**, **sound effects**, **ghost piece**, **hold piece**  
- направя **икона и GitHub cover image**  
- създам **релийз версия** с EXE

Само кажи! 😊
