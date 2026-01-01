import tkinter as tk
from tkinter import ttk, messagebox
from models import Task
from service import TaskService
from storage import FileManager

class TaskOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Organizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize services
        self.service = TaskService()
        self.storage = FileManager()
        self.load_saved_tasks()
        
        # Create UI
        self.create_widgets()
        self.refresh_task_list()
    
    def load_saved_tasks(self):
        """Load tasks from storage"""
        saved_tasks = self. storage.load_tasks()
        for t in saved_tasks: 
            task = Task(t["title"], t["description"], t["deadline"], t["priority"])
            task.status = t["status"]
            self.service.tasks.append(task)
    
    def create_widgets(self):
        """Create all UI components"""
        
        # === Header Frame ===
        header_frame = tk.Frame(self. root, bg="#4a90d9", pady=15)
        header_frame.pack(fill=tk.X)
        
        title_label = tk. Label(
            header_frame, 
            text="📋 Smart Task Organizer", 
            font=("Arial", 20, "bold"),
            bg="#4a90d9", 
            fg="white"
        )
        title_label.pack()
        
        # === Input Frame ===
        input_frame = tk.LabelFrame(self. root, text="إضافة مهمة جديدة", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        tk.Label(input_frame, text="العنوان: ").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry. grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        tk.Label(input_frame, text="الوصف:").grid(row=0, column=2, sticky="w")
        self.desc_entry = tk. Entry(input_frame, width=30)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Deadline
        tk.Label(input_frame, text="الموعد النهائي:").grid(row=1, column=0, sticky="w")
        self.deadline_entry = tk.Entry(input_frame, width=30)
        self.deadline_entry.insert(0, "YYYY-MM-DD")
        self.deadline_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Priority
        tk.Label(input_frame, text="الأولوية:").grid(row=1, column=2, sticky="w")
        self.priority_combo = ttk. Combobox(input_frame, values=["High", "Medium", "Low"], width=27)
        self.priority_combo.set("Medium")
        self.priority_combo.grid(row=1, column=3, padx=5, pady=5)
        
        # Add Button
        add_btn = tk.Button(
            input_frame, 
            text="➕ إضافة مهمة", 
            command=self.add_task,
            bg="#28a745", 
            fg="white",
            font=("Arial", 10, "bold")
        )
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # === Task List Frame ===
        list_frame = tk.LabelFrame(self.root, text="قائمة المهام", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for tasks
        columns = ("title", "description", "deadline", "priority", "status")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.task_tree. heading("title", text="العنوان")
        self.task_tree.heading("description", text="الوصف")
        self.task_tree.heading("deadline", text="الموعد النهائي")
        self.task_tree. heading("priority", text="الأولوية")
        self.task_tree. heading("status", text="الحالة")
        
        self. task_tree.column("title", width=150)
        self.task_tree. column("description", width=200)
        self.task_tree.column("deadline", width=100)
        self.task_tree.column("priority", width=80)
        self.task_tree. column("status", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree. configure(yscrollcommand=scrollbar.set)
        
        self.task_tree. pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk. RIGHT, fill=tk.Y)
        
        # === Action Buttons Frame ===
        action_frame = tk.Frame(self.root, pady=10)
        action_frame.pack(fill=tk. X)
        
        complete_btn = tk. Button(
            action_frame, 
            text="✅ إكمال المهمة", 
            command=self.complete_task,
            bg="#17a2b8", 
            fg="white"
        )
        complete_btn.pack(side=tk. LEFT, padx=5)
        
        delete_btn = tk. Button(
            action_frame, 
            text="🗑️ حذف المهمة", 
            command=self.delete_task,
            bg="#dc3545", 
            fg="white"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk. Button(
            action_frame, 
            text="💾 حفظ المهام", 
            command=self.save_tasks,
            bg="#6c757d", 
            fg="white"
        )
        save_btn. pack(side=tk.RIGHT, padx=5)
    
    def add_task(self):
        """Add a new task"""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        deadline = self.deadline_entry. get().strip()
        priority = self. priority_combo.get()
        
        if not title or not deadline or deadline == "YYYY-MM-DD":
            messagebox.showwarning("تحذير", "الرجاء إدخال العنوان والموعد النهائي!")
            return
        
        task = Task(title, description, deadline, priority)
        self.service.tasks.append(task)
        
        # Clear entries
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk. END)
        self.deadline_entry.insert(0, "YYYY-MM-DD")
        
        self.refresh_task_list()
        messagebox.showinfo("نجاح", "تمت إضافة المهمة بنجاح!")
    
    def complete_task(self):
        """Mark selected task as completed"""
        selected = self.task_tree.selection()
        if not selected: 
            messagebox.showwarning("تحذير", "الرجاء اختيار مهمة!")
            return
        
        index = self.task_tree.index(selected[0])
        self.service.mark_completed(index)
        self.refresh_task_list()
        messagebox.showinfo("نجاح", "تم إكمال المهمة!")
    
    def delete_task(self):
        """Delete selected task"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "الرجاء اختيار مهمة!")
            return
        
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف هذه المهمة؟"):
            index = self. task_tree.index(selected[0])
            self.service.delete_task(index)
            self.refresh_task_list()
    
    def save_tasks(self):
        """Save tasks to storage"""
        self.storage.save_tasks(self.service.tasks)
        messagebox.showinfo("نجاح", "تم حفظ المهام!")
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        for item in self.task_tree.get_children():
            self.task_tree. delete(item)
        
        for task in self.service. tasks:
            self.task_tree. insert("", tk. END, values=(
                task.title,
                task.description,
                task. deadline,
                task.priority,
                task.status
            ))


def main():
    root = tk.Tk()
    app = TaskOrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()