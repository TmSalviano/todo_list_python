import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.root.geometry("800x600")
        
        self.init_database()
        self.create_widgets()
        self.refresh_list()
    
    def init_database(self):
        """Initialize the SQLite database"""
        self.conn = sqlite3.connect("todo_gui.sqlite")
        self.cur = self.conn.cursor()
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS todo_items 
            (todo_item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             summary VARCHAR(100), 
             body TEXT,
             created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             completed BOOLEAN DEFAULT FALSE)
        ''')
        self.conn.commit()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        title_label = ttk.Label(main_frame, text="Todo List", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        input_frame = ttk.LabelFrame(main_frame, text="Add New Todo", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        
        ttk.Label(input_frame, text="Summary:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.summary_entry = ttk.Entry(input_frame, width=50)
        self.summary_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        
        ttk.Label(input_frame, text="Details:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.body_text = tk.Text(input_frame, height=4, width=50)
        self.body_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 10), padx=(0, 10))
        
        self.add_btn = ttk.Button(input_frame, text="Add Todo", command=self.add_todo)
        self.add_btn.grid(row=2, column=1, sticky=tk.E)
        
        self.summary_entry.bind('<Return>', lambda e: self.add_todo())
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(controls_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(controls_frame, text="All", variable=self.filter_var, 
                       value="all", command=self.refresh_list).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Radiobutton(controls_frame, text="Active", variable=self.filter_var, 
                       value="active", command=self.refresh_list).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Radiobutton(controls_frame, text="Completed", variable=self.filter_var, 
                       value="completed", command=self.refresh_list).pack(side=tk.LEFT, padx=(5, 10))
        
        
        ttk.Button(controls_frame, text="Clear Completed", 
                  command=self.clear_completed).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(controls_frame, text="Remove All", 
                  command=self.remove_all).pack(side=tk.LEFT, padx=(5, 10))
        
        
        list_frame = ttk.LabelFrame(main_frame, text="Todo Items", padding="10")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        columns = ('summary', 'body', 'created_date')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('summary', text='Summary')
        self.tree.heading('body', text='Details')
        self.tree.heading('created_date', text='Created Date')
        
        self.tree.column('summary', width=200)
        self.tree.column('body', width=300)
        self.tree.column('created_date', width=150)
        
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
        
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(action_frame, text="Mark Complete", 
                  command=self.mark_complete).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Mark Active", 
                  command=self.mark_active).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(action_frame, text="Edit", 
                  command=self.edit_todo).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(action_frame, text="Remove", 
                  command=self.remove_todo).pack(side=tk.LEFT, padx=(5, 0))
    
    def add_todo(self):
        """Add a new todo item"""
        summary = self.summary_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        
        if not summary:
            messagebox.showwarning("Warning", "Please enter a summary for the todo item.")
            return
        
        try:
            self.cur.execute(
                "INSERT INTO todo_items (summary, body) VALUES (?, ?)", 
                (summary, body)
            )
            self.conn.commit()
            
            
            self.summary_entry.delete(0, tk.END)
            self.body_text.delete("1.0", tk.END)
            
            
            self.refresh_list()
            
            messagebox.showinfo("Success", "Todo item added successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add todo item: {e}")
    
    def refresh_list(self):
        """Refresh the todo list display"""
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        
        filter_type = self.filter_var.get()
        search_text = self.search_var.get().strip()
        
        query = "SELECT todo_item_id, summary, body, created_date, completed FROM todo_items"
        params = []
        
        conditions = []
        if filter_type == "active":
            conditions.append("completed = FALSE")
        elif filter_type == "completed":
            conditions.append("completed = TRUE")
        
        if search_text:
            conditions.append("(summary LIKE ? OR body LIKE ?)")
            params.extend([f'%{search_text}%', f'%{search_text}%'])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_date DESC"
        
        try:
            self.cur.execute(query, params)
            items = self.cur.fetchall()
            
            for item in items:
                item_id, summary, body, created_date, completed = item
                
                
                display_summary = summary
                if completed:
                    display_summary = f"✓ {summary}"
                
                
                display_body = body[:50] + "..." if len(body) > 50 else body
                
                self.tree.insert('', tk.END, values=(
                    display_summary, display_body, created_date
                ), tags=('completed' if completed else 'active'))
            
            
            self.tree.tag_configure('completed', foreground='gray')
            self.tree.tag_configure('active', foreground='black')
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load todo items: {e}")
    
    def on_search(self, event=None):
        """Handle search functionality"""
        self.refresh_list()
    
    def get_selected_item_id(self):
        """Get the database ID of the selected item"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a todo item first.")
            return None
        
        selected_item = self.tree.item(selection[0])
        summary = selected_item['values'][0]
        
        
        if summary.startswith('✓ '):
            summary = summary[2:]
        
        try:
            self.cur.execute(
                "SELECT todo_item_id FROM todo_items WHERE summary = ?", 
                (summary,)
            )
            result = self.cur.fetchone()
            return result[0] if result else None
        except sqlite3.Error:
            return None
    
    def mark_complete(self):
        """Mark selected item as completed"""
        item_id = self.get_selected_item_id()
        if item_id is None:
            return
        
        try:
            self.cur.execute(
                "UPDATE todo_items SET completed = TRUE WHERE todo_item_id = ?",
                (item_id,)
            )
            self.conn.commit()
            self.refresh_list()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to mark item as complete: {e}")
    
    def mark_active(self):
        """Mark selected item as active"""
        item_id = self.get_selected_item_id()
        if item_id is None:
            return
        
        try:
            self.cur.execute(
                "UPDATE todo_items SET completed = FALSE WHERE todo_item_id = ?",
                (item_id,)
            )
            self.conn.commit()
            self.refresh_list()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to mark item as active: {e}")
    
    def edit_todo(self):
        """Edit selected todo item"""
        item_id = self.get_selected_item_id()
        if item_id is None:
            return
        
        
        try:
            self.cur.execute(
                "SELECT summary, body FROM todo_items WHERE todo_item_id = ?",
                (item_id,)
            )
            result = self.cur.fetchone()
            if not result:
                messagebox.showerror("Error", "Todo item not found.")
                return
            
            current_summary, current_body = result
            
            
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Todo")
            edit_window.geometry("500x400")
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            
            ttk.Label(edit_window, text="Summary:").pack(anchor=tk.W, pady=(10, 5), padx=10)
            summary_entry = ttk.Entry(edit_window, width=60)
            summary_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
            summary_entry.insert(0, current_summary)
            
            
            ttk.Label(edit_window, text="Details:").pack(anchor=tk.W, pady=(10, 5), padx=10)
            body_text = tk.Text(edit_window, height=10, width=60)
            body_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            body_text.insert("1.0", current_body)
            
            def save_changes():
                new_summary = summary_entry.get().strip()
                new_body = body_text.get("1.0", tk.END).strip()
                
                if not new_summary:
                    messagebox.showwarning("Warning", "Summary cannot be empty.")
                    return
                
                try:
                    self.cur.execute(
                        "UPDATE todo_items SET summary = ?, body = ? WHERE todo_item_id = ?",
                        (new_summary, new_body, item_id)
                    )
                    self.conn.commit()
                    edit_window.destroy()
                    self.refresh_list()
                    messagebox.showinfo("Success", "Todo item updated successfully!")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Failed to update todo item: {e}")
            
            
            button_frame = ttk.Frame(edit_window)
            button_frame.pack(fill=tk.X, padx=10, pady=10)
            
            ttk.Button(button_frame, text="Save", command=save_changes).pack(side=tk.RIGHT, padx=(5, 0))
            ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.RIGHT)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load todo item: {e}")
    
    def on_item_double_click(self, event):
        """Handle double-click on todo item"""
        self.edit_todo()
    
    def remove_todo(self):
        """Remove selected todo item"""
        item_id = self.get_selected_item_id()
        if item_id is None:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this todo item?"):
            try:
                self.cur.execute(
                    "DELETE FROM todo_items WHERE todo_item_id = ?",
                    (item_id,)
                )
                self.conn.commit()
                self.refresh_list()
                messagebox.showinfo("Success", "Todo item removed successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to remove todo item: {e}")
    
    def clear_completed(self):
        """Remove all completed todo items"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all completed items?"):
            try:
                self.cur.execute("DELETE FROM todo_items WHERE completed = TRUE")
                self.conn.commit()
                self.refresh_list()
                messagebox.showinfo("Success", "Completed items cleared successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to clear completed items: {e}")
    
    def remove_all(self):
        """Remove all todo items"""
        if messagebox.askyesno("Confirm", "Are you sure you want to remove ALL todo items?"):
            try:
                self.cur.execute("DELETE FROM todo_items")
                self.conn.commit()
                self.refresh_list()
                messagebox.showinfo("Success", "All todo items removed successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to remove all items: {e}")
    
    def __del__(self):
        """Cleanup when the app is closed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()