import tkinter as tk
from tkinter import messagebox, ttk

class BankSystem:
    def __init__(self):
        # Инициализация базы данных (в памяти) с демонстрационным аккаунтом
        self.accounts = {
            "123456": {
                "pin": "1111",
                "balance": 50000.0,
                "history": ["Счет создан. Баланс: 50,000.00 руб."]
            }
        }
        self.current_acc = None

    def authenticate(self, acc_num, pin):
        if acc_num in self.accounts and self.accounts[acc_num]["pin"] == pin:
            self.current_acc = acc_num
            return True
        return False

    def create_account(self, acc_num, pin, initial_deposit):
        if acc_num in self.accounts:
            return False, "Счет с таким номером уже существует."
        if len(acc_num) < 4 or len(pin) < 4:
            return False, "Номер счета и PIN должны содержать минимум 4 символа."
        
        self.accounts[acc_num] = {
            "pin": pin,
            "balance": float(initial_deposit),
            "history": [f"Счет создан. Начальный баланс: {initial_deposit:,.2f} руб."]
        }
        return True, "Счет успешно создан!"

    def deposit(self, amount):
        if amount <= 0:
            return False, "Сумма пополнения должна быть больше нуля."
        self.accounts[self.current_acc]["balance"] += amount
        self.accounts[self.current_acc]["history"].append(f"Пополнение: +{amount:,.2f} руб.")
        return True, f"Успешно пополнено на {amount:,.2f} руб."

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Сумма снятия должна быть больше нуля."
        if self.accounts[self.current_acc]["balance"] < amount:
            return False, "Недостаточно средств на счете."
        self.accounts[self.current_acc]["balance"] -= amount
        self.accounts[self.current_acc]["history"].append(f"Снятие: -{amount:,.2f} руб.")
        return True, f"Успешно снято {amount:,.2f} руб."

    def transfer(self, target_acc, amount):
        if amount <= 0:
            return False, "Сумма перевода должна быть больше нуля."
        if target_acc not in self.accounts:
            return False, "Счет получателя не найден."
        if target_acc == self.current_acc:
            return False, "Нельзя переводить средства на свой же счет."
        if self.accounts[self.current_acc]["balance"] < amount:
            return False, "Недостаточно средств для перевода."

        self.accounts[self.current_acc]["balance"] -= amount
        self.accounts[target_acc]["balance"] += amount
        
        self.accounts[self.current_acc]["history"].append(f"Перевод на счет {target_acc}: -{amount:,.2f} руб.")
        self.accounts[target_acc]["history"].append(f"Перевод со счета {self.current_acc}: +{amount:,.2f} руб.")
        return True, f"Успешно переведено {amount:,.2f} руб. на счет {target_acc}."

    def get_balance(self):
        return self.accounts[self.current_acc]["balance"]

    def get_history(self):
        return self.accounts[self.current_acc]["history"]


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Имитация Банковской Системы")
        self.geometry("450x500")
        self.resizable(False, False)
        
        self.bank = BankSystem()
        
        # Стилизация
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure(bg="#f4f6f9")
        
        # Контейнер для экранов
        self.container = tk.Frame(self, bg="#f4f6f9")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()
        
        # Заголовок
        lbl_title = tk.Label(self.container, text="🔑 Авторизация", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_title.pack(pady=20)
        
        # Номер счета
        tk.Label(self.container, text="Номер счета:", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        entry_acc = ttk.Entry(self.container, font=("Arial", 12))
        entry_acc.pack(fill="x", pady=5)
        entry_acc.insert(0, "123456") # Для теста
        
        # PIN
        tk.Label(self.container, text="PIN-код:", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        entry_pin = ttk.Entry(self.container, show="*", font=("Arial", 12))
        entry_pin.pack(fill="x", pady=5)
        entry_pin.insert(0, "1111") # Для теста
        
        # Кнопка Войти
        btn_login = tk.Button(self.container, text="Войти", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", 
                              relief="flat", activebackground="#27ae60", activeforeground="white",
                              command=lambda: self.handle_login(entry_acc.get(), entry_pin.get()))
        btn_login.pack(fill="x", pady=20)
        
        # Разделитель
        ttk.Separator(self.container, orient="horizontal").pack(fill="x", pady=10)
        
        # Ссылка на создание аккаунта
        btn_reg_screen = tk.Button(self.container, text="Создать новый счет", font=("Arial", 10, "underline"), 
                                   bg="#f4f6f9", fg="#3498db", relief="flat", activebackground="#f4f6f9", activeforeground="#2980b9",
                                   command=self.show_register_screen)
        btn_reg_screen.pack()

    def handle_login(self, acc, pin):
        if self.bank.authenticate(acc, pin):
            self.show_dashboard()
        else:
            messagebox.showerror("Ошибка", "Неверный номер счета или PIN-код.")

    def show_register_screen(self):
        self.clear_container()
        
        lbl_title = tk.Label(self.container, text="🆕 Регистрация счета", font=("Arial", 18, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_title.pack(pady=20)
        
        tk.Label(self.container, text="Придумайте номер счета:", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        entry_acc = ttk.Entry(self.container, font=("Arial", 12))
        entry_acc.pack(fill="x", pady=5)
        
        tk.Label(self.container, text="Придумайте PIN-код:", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        entry_pin = ttk.Entry(self.container, show="*", font=("Arial", 12))
        entry_pin.pack(fill="x", pady=5)
        
        tk.Label(self.container, text="Начальный депозит (руб.):", font=("Arial", 11), bg="#f4f6f9").pack(anchor="w", pady=2)
        entry_dep = ttk.Entry(self.container, font=("Arial", 12))
        entry_dep.pack(fill="x", pady=5)
        entry_dep.insert(0, "1000")
        
        btn_register = tk.Button(self.container, text="Зарегистрироваться", font=("Arial", 12, "bold"), bg="#3498db", fg="white", 
                                 relief="flat", activebackground="#2980b9", activeforeground="white",
                                 command=lambda: self.handle_register(entry_acc.get(), entry_pin.get(), entry_dep.get()))
        btn_register.pack(fill="x", pady=20)
        
        btn_back = tk.Button(self.container, text="Назад к авторизации", font=("Arial", 10), bg="#f4f6f9", fg="#7f8c8d", 
                             relief="flat", command=self.show_login_screen)
        btn_back.pack()

    def handle_register(self, acc, pin, dep):
        try:
            dep_val = float(dep)
            if dep_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма депозита должна быть корректным числом >= 0.")
            return

        success, msg = self.bank.create_account(acc, pin, dep_val)
        if success:
            messagebox.showinfo("Успех", msg)
            self.show_login_screen()
        else:
            messagebox.showerror("Ошибка", msg)

    def show_dashboard(self):
        self.clear_container()
        
        # Верхняя панель инфо
        lbl_acc = tk.Label(self.container, text=f"Счет: №{self.bank.current_acc}", font=("Arial", 11), bg="#f4f6f9", fg="#7f8c8d")
        lbl_acc.pack(anchor="w")
        
        self.lbl_balance = tk.Label(self.container, text=f"{self.bank.get_balance():,.2f} руб.", font=("Arial", 22, "bold"), bg="#f4f6f9", fg="#2c3e50")
        self.lbl_balance.pack(anchor="w", pady=5)
        
        ttk.Separator(self.container, orient="horizontal").pack(fill="x", pady=10)
        
        # Кнопки операций
        btn_frame = tk.Frame(self.container, bg="#f4f6f9")
        btn_frame.pack(fill="x", pady=5)
        
        btn_dep = tk.Button(btn_frame, text="💵 Пополнить", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", relief="flat", command=self.open_deposit_dialog)
        btn_dep.pack(side="left", expand=True, fill="x", padx=2)
        
        btn_wd = tk.Button(btn_frame, text="💸 Снять", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", command=self.open_withdraw_dialog)
        btn_wd.pack(side="left", expand=True, fill="x", padx=2)
        
        btn_tx = tk.Button(btn_frame, text="🔄 Перевод", font=("Arial", 10, "bold"), bg="#9b59b6", fg="white", relief="flat", command=self.open_transfer_dialog)
        btn_tx.pack(side="left", expand=True, fill="x", padx=2)

        ttk.Separator(self.container, orient="horizontal").pack(fill="x", pady=15)
        
        # История операций
        tk.Label(self.container, text="🗒 История операций:", font=("Arial", 11, "bold"), bg="#f4f6f9", fg="#2c3e50").pack(anchor="w")
        
        self.history_list = tk.Listbox(self.container, font=("Arial", 10), bg="white", height=8, relief="flat", highlightthickness=1, highlightbackground="#bdc3c7")
        self.history_list.pack(fill="both", expand=True, pady=5)#
        self.update_history_view()
        
        # Выход
        btn_logout = tk.Button(self.container, text="Выйти из системы", font=("Arial", 10), bg="#f4f6f9", fg="#e74c3c", relief="flat", command=self.show_login_screen)
        btn_logout.pack(pady=10)

    def update_balance_view(self):
        self.lbl_balance.config(text=f"{self.bank.get_balance():,.2f} руб.")
        self.update_history_view()

    def update_history_view(self):
        self.history_list.delete(0, tk.END)
        for log in reversed(self.bank.get_history()):
            self.history_list.insert(tk.END, log)

    def _get_amount_dialog(self, title, prompt):
        # Быстрое кастомное диалоговое окно для ввода суммы
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(dialog, text=prompt, font=("Arial", 10)).pack(pady=10)
        entry = ttk.Entry(dialog, font=("Arial", 11))
        entry.pack(pady=5, padx=20, fill="x")
        entry.focus_set()
        
        result = [None]
        
        def on_ok():
            result[0] = entry.get()
            dialog.destroy()
            
        btn = ttk.Button(dialog, text="Подтвердить", command=on_ok)
        btn.pack(pady=10)
        
        self.wait_window(dialog)
        return result[0]

    def open_deposit_dialog(self):
        val = self._get_amount_dialog("Пополнение", "Введите сумму для пополнения:")
        if val is not None:
            try:
                amount = float(val)
                success, msg = self.bank.deposit(amount)
                if success:
                    messagebox.showinfo("Успех", msg)
                    self.update_balance_view()
                else:
                    messagebox.showerror("Ошибка", msg)
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")

    def open_withdraw_dialog(self):
        val = self._get_amount_dialog("Снятие средств", "Введите сумму для снятия:")
        if val is not None:
            try:
                amount = float(val)
                success, msg = self.bank.withdraw(amount)
                if success:
                    messagebox.showinfo("Успех", msg)
                    self.update_balance_view()
                else:
                    messagebox.showerror("Ошибка", msg)
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")

    def open_transfer_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Перевод средств")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(dialog, text="Номер счета получателя:", font=("Arial", 10)).pack(pady=5)
        entry_target = ttk.Entry(dialog, font=("Arial", 11))
        entry_target.pack(pady=2, padx=20, fill="x")
        
        tk.Label(dialog, text="Сумма перевода:", font=("Arial", 10)).pack(pady=5)
        entry_amount = ttk.Entry(dialog, font=("Arial", 11))
        entry_amount.pack(pady=2, padx=20, fill="x")
        
        def on_transfer():
            target = entry_target.get()
            val = entry_amount.get()
            try:
                amount = float(val)
                success, msg = self.bank.transfer(target, amount)
                if success:
                    messagebox.showinfo("Успех", msg)
                    self.update_balance_view()
                    dialog.destroy()
                else:
                    messagebox.showerror("Ошибка", msg)
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")
                
        ttk.Button(dialog, text="Перевести", command=on_transfer).pack(pady=15)
        self.wait_window(dialog)


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
