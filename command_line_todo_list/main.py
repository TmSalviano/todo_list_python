import sqlite3, sys

# primary key / summary (logical key) / body
def exit_func(l):
    if len(sys.argv) <= l:
        print("""
            add or -a [SUMMARY] [BODY] to add todo item
            remove or -r [ID] to remove todo item by ID
            remove-all or -ra to remove all todo items
            view or -v to view all todo items
            view [ID] to view specific todo item
            update or -u [ID] [NEW_SUMMARY] [NEW_BODY] to update todo item

                ID = unique identifier of the todo item
                SUMMARY = short description of the todo item
                BODY = detailed description of the todo item
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
            try:
                item_id = int(sys.argv[2])
                cur.execute('DELETE FROM todo_items WHERE todo_item_id = ?', (item_id,))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Removed todo item with ID: {item_id}")
                else:
                    print(f"No todo item found with ID: {item_id}")
            except ValueError:
                print("Error: ID must be an integer")
                
        case 'remove-all' | '-ra':
            cur.execute('DELETE FROM todo_items')
            conn.commit()
            print("Removed all todo items")
                    
        case 'view' | '-v':
            if len(sys.argv) > 2:
                try:
                    item_id = int(sys.argv[2])
                    cur.execute('SELECT * FROM todo_items WHERE todo_item_id = ?', (item_id,))
                    result = cur.fetchone()
                    if result:
                        print(f"ID: {result[0]}, Summary: {result[1]}, Body: {result[2]}")
                    else:
                        print(f"No todo item found with ID: {item_id}")
                except ValueError:
                    print("Error: ID must be an integer")
            else:
                cur.execute("SELECT * FROM todo_items")
                results = cur.fetchall()
                if results:
                    for todo_item in results:
                        print(f"ID: {todo_item[0]}, Summary: {todo_item[1]}, Body: {todo_item[2]}")
                else:
                    print("No todo items found")
        
        case 'update' | '-u':
            exit_func(4)
            try:
                item_id = int(sys.argv[2])
                new_summary = sys.argv[3]
                new_body = sys.argv[4]
                cur.execute('UPDATE todo_items SET summary = ?, body = ? WHERE todo_item_id = ?', 
                           (new_summary, new_body, item_id))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Updated todo item with ID: {item_id}")
                else:
                    print(f"No todo item found with ID: {item_id}")
            except ValueError:
                print("Error: ID must be an integer")
                
        case _:
            print("Invalid command")
            
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()