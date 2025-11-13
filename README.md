# Todo List Applications

Three todo list implementations using different Python technologies.

## 🚀 Applications

### 1. CLI Todo List (Python + SQLite)
Command-line task manager with SQLite backend.

**Features:**
- Add, view, update, delete tasks
- SQLite database persistence
- Simple command syntax

**Usage:**
```bash
cd cli-todo
python todo.py add "Buy groceries" "Milk, eggs, bread"
python todo.py view
python todo.py remove 1
python todo.py update 1 "New summary" "New details"
```

### 2. GUI Todo List (Tkinter + SQLite)
Desktop application with modern interface.

**Features:**
- Graphical interface with Tkinter
- Search and filter tasks
- Mark tasks complete/incomplete
- Rich text details
- Persistent storage

**Usage:**
```bash
cd gui-todo
python todo_app.py
```

### 3. Web Todo List (Django) - Coming Soon
Full web application with user authentication.

**Planned Features:**
- User accounts
- Task categories and due dates
- REST API
- Responsive design

## 📁 Project Structure
```
todo-apps/
├── cli-todo/          # Command line version
├── gui-todo/          # Desktop GUI version  
└── web-todo/          # Web version (future)
```

## 🛠️ Technologies
- **CLI**: Python, SQLite
- **GUI**: Python, Tkinter, SQLite  
- **Web**: Django (planned)

## 🎯 Learning Goals
- Different UI approaches (CLI, GUI, Web)
- SQLite database integration
- Python application architecture

Each app is self-contained and can run independently.
