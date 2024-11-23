import tkinter as tk
from tkinter import messagebox
import math  # Thêm thư viện toán học

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy Tính Casio")
root.geometry("400x600")
root.configure(bg="#1e1e1e")

# Biến lưu trữ biểu thức và bộ nhớ
expression = ""
memory = 0  # Bộ nhớ để lưu trữ giá trị của M+

# Hàm cập nhật biểu thức
def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

# Hàm xử lý khi nhấn nút sin, cos, tan, cot
def press_function(func_name):
    global expression
    expression += func_name + "("  # Thêm dấu "(" sau tên hàm
    equation.set(expression)

# Hàm tính kết quả
def equalpress():
    global expression
    try:
        # Thay thế các hàm lượng giác, thêm chuyển đổi sang radian
        modified_expression = expression.replace("sin", "math.sin(math.radians") \
                                         .replace("cos", "math.cos(math.radians") \
                                         .replace("tan", "math.tan(math.radians") \
                                         .replace("cot", "1/math.tan(math.radians") \
                                         .replace("√", "**0.5") \
                                         .replace("^", "**")
        # Thêm dấu đóng ngoặc cho các hàm lượng giác
        modified_expression = modified_expression.replace(")", "))")
        total = str(eval(modified_expression))
        equation.set(total)
        expression = total
    except Exception as e:
        equation.set("Lỗi")
        expression = ""

# Hàm xóa toàn bộ biểu thức
def clear():
    global expression
    expression = ""
    equation.set("")

# Hàm M+ để cộng giá trị hiện tại vào bộ nhớ
def memory_plus():
    global expression, memory
    try:
        memory += eval(expression)  # Cộng giá trị hiện tại vào bộ nhớ
        equation.set("M+")
        expression = ""
    except:
        equation.set("Lỗi")
        expression = ""

# Hàm MR để lấy giá trị từ bộ nhớ
def memory_recall():
    global memory
    equation.set(str(memory))
    expression = str(memory)

# Hàm DEL để xóa ký tự cuối cùng
def delete_last():
    global expression
    expression = expression[:-1]
    equation.set(expression)

# Cấu hình hiển thị biểu thức
equation = tk.StringVar()
entry_field = tk.Entry(root, textvariable=equation, font=('Arial', 20), bd=10, insertwidth=2, width=22, borderwidth=4, justify="right")
entry_field.grid(row=0, column=0, columnspan=5, pady=20)

# Danh sách các nút mô phỏng giao diện Casio
buttons = [
    ("(", 1, 0), (")", 1, 1), ("M+", 1, 2), ("DEL", 1, 3), ("AC", 1, 4),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3), ("√", 2, 4),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3), ("^", 3, 4),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3), ("MR", 4, 4),
    ("0", 5, 0), (".", 5, 1), ("+", 5, 2), ("=", 5, 3),
    ("sin", 6, 0), ("cos", 6, 1), ("tan", 6, 2), ("cot", 6, 3)
]

# Tạo các nút theo kiểu máy tính Casio
for (text, row, col) in buttons:
    if text in ["sin", "cos", "tan", "cot"]:
        button = tk.Button(root, text=text, command=lambda t=text: press_function(t), font=('Arial', 18, 'bold'), fg="white", bg="#333333", height=2, width=6)
    elif text == "=":
        button = tk.Button(root, text=text, command=equalpress, font=('Arial', 18, 'bold'), fg="white", bg="#ff9500", height=2, width=6)
    elif text == "AC":
        button = tk.Button(root, text=text, command=clear, font=('Arial', 18, 'bold'), fg="white", bg="#ff3b30", height=2, width=6)
    elif text == "M+":
        button = tk.Button(root, text=text, command=memory_plus, font=('Arial', 18, 'bold'), fg="white", bg="#333333", height=2, width=6)
    elif text == "MR":
        button = tk.Button(root, text=text, command=memory_recall, font=('Arial', 18, 'bold'), fg="white", bg="#333333", height=2, width=6)
    elif text == "DEL":
        button = tk.Button(root, text=text, command=delete_last, font=('Arial', 18, 'bold'), fg="white", bg="#333333", height=2, width=6)
    else:
        button = tk.Button(root, text=text, command=lambda t=text: press(t), font=('Arial', 18, 'bold'), fg="white", bg="#333333", height=2, width=6)
    button.grid(row=row, column=col, padx=5, pady=5)

root.mainloop()
