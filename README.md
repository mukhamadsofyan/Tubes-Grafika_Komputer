# 🎨 Tubes Grafika Komputer

Final project mata kuliah **Grafika Komputer** yang dibuat menggunakan **Python + PyOpenGL + GLUT**.
Repository ini berisi implementasi konsep dasar grafika komputer dalam bentuk aplikasi interaktif **2D dan 3D**.

Project ini terdiri dari dua modul utama:

* **Modul A** — Aplikasi grafika 2D untuk menggambar objek, clipping window, transformasi, dan interaksi keyboard/mouse.
* **Modul B** — Aplikasi grafika 3D untuk menampilkan dan memanipulasi objek 3D seperti **cube** dan **pyramid**.

---

# 📌 Project Overview

Repository **Tubes Grafika Komputer** dikembangkan sebagai implementasi praktis dari materi grafika komputer.

Konsep yang diimplementasikan:

* Rendering objek 2D
* Rendering objek 3D
* Transformasi geometri
* Clipping window
* Interaksi mouse dan keyboard
* Pewarnaan objek
* Lighting pada objek 3D

Tujuan dari project ini adalah memahami bagaimana objek grafis dirender dan dimanipulasi menggunakan **OpenGL** di Python.

---

# 🚀 Modules

## 🧩 Modul A — Interactive 2D Drawing Application

Aplikasi ini digunakan untuk menggambar objek 2D secara interaktif dengan dukungan transformasi dan clipping.

### ✨ Features

* Menggambar **Point**
* Menggambar **Line**
* Menggambar **Square**
* Menggambar **Ellipse**
* **Window clipping**
* **Translate object**
* **Rotate object**
* **Scale object**
* **Zoom in / Zoom out**
* **Undo object**
* **Delete object**
* **Move clipping window**
* **Snap to grid**
* Pengaturan **warna**
* Pengaturan **thickness**

### 🧠 Implemented Concepts

* 2D coordinate normalization
* Cohen-Sutherland clipping
* Translation
* Rotation
* Scaling
* Windowing
* Object selection

---

## 🧊 Modul B — Interactive 3D Object Viewer

Aplikasi ini digunakan untuk menampilkan dan memanipulasi objek 3D menggunakan OpenGL.

### ✨ Features

* Menampilkan **Cube**
* Menampilkan **Pyramid**
* Rotasi objek dengan mouse
* Translasi objek
* Zoom in / zoom out
* Pencahayaan dasar
* Smooth shading
* Reset transformasi

### 🧠 Implemented Concepts

* 3D transformation
* Perspective projection
* Lighting
* Camera interaction
* Mouse-based rotation
* Keyboard interaction

---

# 🎮 Controls

## Modul A — Drawing Controls

### Drawing Mode

* `1` → Point
* `2` → Line
* `3` → Square
* `4` → Ellipse
* `W` → Set window clipping
* `Q` → Exit window mode

### Transformations

* `T` → Translate
* `O` → Rotate
* `S` → Scale
* `U` → Zoom out
* `I` → Zoom in

### Object Management

* `D` → Delete object
* `Z` → Undo

### Appearance

* `R` → Red
* `G` → Green
* `B` → Blue
* `+` → Increase thickness
* `-` → Decrease thickness

### Utility

* `M` → Move window
* `Shift + G` → Snap grid
* `X` → Reset window
* `H` → Show shortcut help

### Mouse

* **Left Click** → Draw object
* **Drag** → Move object / window

---

## Modul B — 3D Controls

### Mouse

* **Left Drag** → Rotasi objek
* **Right Drag** → Translasi objek
* **Scroll** → Zoom

### Keyboard

#### Object

* `1` → Cube
* `2` → Pyramid
* `R` → Reset transformasi

#### Rotation

* `W / S` → Rotasi sumbu X
* `A / D` → Rotasi sumbu Y

#### Translation

* `I / K` → Atas / bawah
* `J / L` → Kiri / kanan

#### Zoom

* `Z` → Zoom in
* `X` → Zoom out

---

# 🧰 Tech Stack

| Technology | Description           |
| ---------- | --------------------- |
| Python     | Programming Language  |
| OpenGL     | Graphics Rendering    |
| PyOpenGL   | Python OpenGL Binding |
| GLUT       | Window Management     |

---

# 📁 Project Structure

```bash
Tubes-Grafika-Komputer/
│
├── modul_a.py
├── modul_b.py
└── README.md
```

---

# ⚙️ Requirements

Sebelum menjalankan project, install:

* Python 3.x
* PyOpenGL
* PyOpenGL_accelerate
* FreeGLUT

---

# 🛠 Installation

### 1 Clone Repository

```bash
git clone https://github.com/username/tubes-grafika-komputer.git
```

### 2 Masuk ke Folder Project

```bash
cd tubes-grafika-komputer
```

### 3 Install Dependencies

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

---

# ▶️ Run Program

### Jalankan Modul A

```bash
python modul_a.py
```

### Jalankan Modul B

```bash
python modul_b.py
```

---

# 📚 Learning Outcomes

Project ini dibuat untuk memahami:

* Primitive drawing
* Object transformation
* Window clipping
* Interactive graphics
* 3D rendering
* OpenGL lighting
* Event-driven graphics programming

---

# 🎯 Project Purpose

Project ini dibuat sebagai:

* **Tugas Besar Mata Kuliah Grafika Komputer**
* Implementasi konsep grafika komputer secara praktis
* Latihan penggunaan **OpenGL dalam Python**
* Portfolio project di bidang **Computer Graphics**

---

# 👨‍💻 Author

**Mukhamad Sofyan**
GitHub: https://github.com/mukhamadsofyan

---

# 🤝 Contributors

Project ini dikembangkan oleh:

* **Mukhamad Sofyan**
* **Moh. Ravlindo Saputra**
* **Febrian Richo Pradana**

---

# 📄 License

Project ini dibuat untuk **tujuan pembelajaran dan portfolio akademik**.
