import mysql.connector
from tkinter import *
from tkinter import messagebox

# Подключение к базе данных
db = mysql.connector.connect(
    host="localhost",
    user="root",  # замените на ваше имя пользователя
    password="12543hRGB2001",  # замените на ваш пароль
    database="inventory_db"
)

cursor = db.cursor()

# Функции для работы с БД
def add_product_window():
    add_window = Toplevel(root)
    add_window.title("Добавить товар")
    add_window.geometry("400x200")

    label_name = Label(add_window, text="Наименование")
    label_name.grid(row=0, column=0, padx=10, pady=10)
    entry_name = Entry(add_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_quantity = Label(add_window, text="Количество")
    label_quantity.grid(row=1, column=0, padx=10, pady=10)
    entry_quantity = Entry(add_window)
    entry_quantity.grid(row=1, column=1, padx=10, pady=10)

    label_warehouse = Label(add_window, text="Склад")
    label_warehouse.grid(row=2, column=0, padx=10, pady=10)
    entry_warehouse = Entry(add_window)
    entry_warehouse.grid(row=2, column=1, padx=10, pady=10)

    def add_product():
        name = entry_name.get()
        quantity = entry_quantity.get()
        warehouse = entry_warehouse.get()

        if name and quantity and warehouse:
            cursor.execute("INSERT INTO products (name, quantity, warehouse) VALUES (%s, %s, %s)", (name, quantity, warehouse))
            db.commit()
            refresh_listbox()
            add_window.destroy()
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")

    button_add = Button(add_window, text="Добавить", command=add_product)
    button_add.grid(row=3, columnspan=2, pady=10)

def update_product_window():
    selected_product = listbox_products.curselection()
    if not selected_product:
        messagebox.showwarning("Ошибка", "Выберите товар для изменения")
        return

    id, name, quantity, warehouse = listbox_products.get(selected_product)

    update_window = Toplevel(root)
    update_window.title("Изменить товар")
    update_window.geometry("400x200")

    label_name = Label(update_window, text="Наименование")
    label_name.grid(row=0, column=0, padx=10, pady=10)
    entry_name = Entry(update_window)
    entry_name.insert(END, name)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    label_quantity = Label(update_window, text="Количество")
    label_quantity.grid(row=1, column=0, padx=10, pady=10)
    entry_quantity = Entry(update_window)
    entry_quantity.insert(END, quantity)
    entry_quantity.grid(row=1, column=1, padx=10, pady=10)

    label_warehouse = Label(update_window, text="Склад")
    label_warehouse.grid(row=2, column=0, padx=10, pady=10)
    entry_warehouse = Entry(update_window)
    entry_warehouse.insert(END, warehouse)
    entry_warehouse.grid(row=2, column=1, padx=10, pady=10)

    def update_product():
        new_name = entry_name.get()
        new_quantity = entry_quantity.get()
        new_warehouse = entry_warehouse.get()

        if new_name and new_quantity and new_warehouse:
            cursor.execute("UPDATE products SET name=%s, quantity=%s, warehouse=%s WHERE id=%s",
                           (new_name, new_quantity, new_warehouse, id))
            db.commit()
            refresh_listbox()
            update_window.destroy()
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")

    button_update = Button(update_window, text="Сохранить изменения", command=update_product)
    button_update.grid(row=3, columnspan=2, pady=10)

def delete_product():
    selected_product = listbox_products.curselection()
    if not selected_product:
        messagebox.showwarning("Ошибка", "Выберите товар для удаления")
        return

    id = listbox_products.get(selected_product)[0]
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()
    refresh_listbox()

def refresh_listbox():
    listbox_products.delete(0, END)
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        listbox_products.insert(END, row)

# Создание интерфейса
root = Tk()
root.title("Управление складом")
root.geometry("600x400")

# Кнопки действий
button_add = Button(root, text="Добавить", command=add_product_window)
button_add.grid(row=0, column=0, padx=10, pady=10)

button_update = Button(root, text="Изменить", command=update_product_window)
button_update.grid(row=0, column=1, padx=10, pady=10)

button_delete = Button(root, text="Удалить", command=delete_product)
button_delete.grid(row=0, column=2, padx=10, pady=10)

# Список продуктов
listbox_products = Listbox(root, selectmode=SINGLE, width=50)
listbox_products.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

refresh_listbox()

root.mainloop()

# Закрываем соединение с БД при выходе
cursor.close()
db.close()