import sqlite3, sys

# primary key / summary (logical key) / body
def exit_func(l):
    if len(sys.argv) <= l:
        print("""
            add or -a to add todo item
            remove or -r [SUMMARY]/all to remove todo item
            view or -v to view todo items

                SUMMARY = short description of the todo item
            """)
        sys.exit()

exit_func(1)

conn = sqlite3.connect("database.sqlite")
cur = conn.cursor()
    
cur.execute('''
            CREATE TABLE IF NOT EXISTS todo_items 
            (todo_item_id INTEGER PRIMARY KEY AUTOINCREMENT, summary VARCHAR(100), body TEXT);
            ''')

try:
    match sys.argv[1]:
        case 'add' | '-a':
            exit_func(3)
            summary = sys.argv[2]
            body = sys.argv[3]
            cur.execute("INSERT INTO todo_items (summary, body) VALUES (?, ?)", (summary, body))
            conn.commit()
            print(f"Added todo item: {summary}")
            
        case 'remove' | '-r':
            exit_func(2)
            summary = sys.argv[2] 
            if summary == 'all':
                cur.execute('DELETE FROM todo_items')
                conn.commit()
                print("Removed all todo items")
            else:
                cur.execute('DELETE FROM todo_items WHERE summary = ?', (summary,))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Removed todo item: {summary}")
                else:
                    print(f"No todo item found with summary: {summary}")
                    
        case 'view' | '-v':
            if len(sys.argv) > 2 and sys.argv[2] != 'all':
                summary = sys.argv[2]
                cur.execute('SELECT * FROM todo_items WHERE summary = ?', (summary,))
            else:
                cur.execute("SELECT * FROM todo_items")
                
            results = cur.fetchall()
            if results:
                for todo_item in results:
                    print(f"ID: {todo_item[0]}, Summary: {todo_item[1]}, Body: {todo_item[2]}")
            else:
                print("No todo items found")
                
        case _:
            print("Invalid command")
            
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()