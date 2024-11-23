import tkinter as tk
from tkinter import messagebox, Menu
import psycopg2
from psycopg2 import sql


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Database connection fields
        self.db_name = tk.StringVar(value='test')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='danhsach')

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Menu items
        menu_bar.add_command(label="View Data", command=self.load_data)
        menu_bar.add_command(label="Add Data", command=self.show_insert_frame)
        menu_bar.add_command(label="Update/Delete Data", command=self.show_update_frame)
        menu_bar.add_command(label="Search Data", command=self.show_search_frame)

        # Connection section
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Query section
        self.query_frame = tk.Frame(self.root)
        self.query_frame.pack(pady=10)

        tk.Label(self.query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.query_frame, text="Load Data", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        self.data_display = tk.Text(self.root, height=10, width=50)
        self.data_display.pack(pady=10)

        # Insert frame
        self.insert_frame = tk.Frame(self.root)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(self.insert_frame, text="Ho ten:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.insert_frame, text="Dia chi:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, columnspan=2, pady=10)

        # Update/Delete frame
        self.update_frame = tk.Frame(self.root)

        self.update_id = tk.StringVar()
        self.update_name = tk.StringVar()
        self.update_address = tk.StringVar()

        tk.Label(self.update_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.update_frame, textvariable=self.update_id).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.update_frame, text="Ho ten:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.update_frame, textvariable=self.update_name).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.update_frame, text="Dia chi:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.update_frame, textvariable=self.update_address).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.update_frame, text="Update Data", command=self.update_data).grid(row=3, column=0, pady=10)
        tk.Button(self.update_frame, text="Delete Data", command=self.delete_data).grid(row=3, column=1, pady=10)

        # Search frame
        self.search_frame = tk.Frame(self.root)

        self.search_keyword = tk.StringVar()

        tk.Label(self.search_frame, text="Từ khóa:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.search_frame, textvariable=self.search_keyword).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.search_frame, text="Tìm kiếm", command=self.search_data).grid(row=0, column=2, padx=5, pady=5)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            self.query_frame.pack(pady=10)
            self.insert_frame.pack_forget()
            self.update_frame.pack_forget()
            self.search_frame.pack_forget()

            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            self.data_display.delete(1.0, tk.END)
            self.data_display.insert(tk.END, f"{'ID':<5} {'Họ Tên':<20} {'Địa Chỉ':<30}\n")
            self.data_display.insert(tk.END, "-" * 50 + "\n")
            for row in rows:
                self.data_display.insert(tk.END, f"{row[0]:<5} {row[1]:<20} {row[2]:<30}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, diachi) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(insert_query, (self.column1.get(), self.column2.get()))
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def update_data(self):
        try:
            update_query = sql.SQL("UPDATE {} SET hoten = %s, diachi = %s WHERE id = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(update_query, (self.update_name.get(), self.update_address.get(), self.update_id.get()))
            self.conn.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating data: {e}")

    def delete_data(self):
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (self.update_id.get(),))
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error deleting data: {e}")

    def search_data(self):
        try:
            self.query_frame.pack_forget()
            self.insert_frame.pack_forget()
            self.update_frame.pack_forget()
            self.search_frame.pack(pady=10)

            search_query = sql.SQL("SELECT * FROM {} WHERE hoten ILIKE %s OR diachi ILIKE %s").format(sql.Identifier(self.table_name.get()))
            keyword = f"%{self.search_keyword.get()}%"
            self.cur.execute(search_query, (keyword, keyword))
            rows = self.cur.fetchall()

            self.data_display.delete(1.0, tk.END)
            if rows:
                for row in rows:
                    self.data_display.insert(tk.END, f"{row}\n")
            else:
                self.data_display.insert(tk.END, "Không tìm thấy kết quả.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")

    def show_insert_frame(self):
        self.query_frame.pack_forget()
        self.update_frame.pack_forget()
        self.search_frame.pack_forget()
        self.insert_frame.pack(pady=10)

    def show_update_frame(self):
        self.query_frame.pack_forget()
        self.insert_frame.pack_forget()
        self.search_frame.pack_forget()
        self.update_frame.pack(pady=10)

    def show_search_frame(self):
        self.query_frame.pack_forget()
        self.insert_frame.pack_forget()
        self.update_frame.pack_forget()
        self.search_frame.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
