import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

color_palette = [
    '#FF6B6B',  
    '#FFE66D',  
    '#4ECDC4',  
    '#95E1D3',  
    '#A8E6CF',  
    '#FFB6B9',  
    '#C7CEEA',  
    '#B4A7D6',  
    '#FFDAC1',  
    '#FF8B94',  
    '#6C5CE7', 
    '#00B894',  
    '#FDCB6E',  
    '#E17055',  
    '#74B9FF',  
    '#A29BFE',  
    '#FD79A8',  
    '#DCDDE1',  
    '#00CEC9', 
    '#FFEAA7',  
    ]

# Fungsi untuk membaca file dan membangun papan
def read_file(filename: str) :
    if not os.path.exists(filename) :
        raise FileNotFoundError(f"File '{filename}' not found!")
    
    with open(filename, 'r') as f :
        lines = f.readlines()
    
    board = []
    for line in lines:
        line = line.strip()
        if line :
            board.append(list(line))
    
    if not board :
        raise ValueError('Board is empty!')
    
    n = len(board)
    for row in board :
        if len(row)!=n:
            raise ValueError("Board must be square (NxN)!")
     
    return board

# Fungsi untuk menyimpan solusi
def save_text(solution: list[list[str]], filename: str) :
    with open(filename, 'w') as f :
        for row in solution :
            f.write(''.join(row) + '\n')

# Fungsi untuk mengambil warna
def get_color(char: str, map: dict) :
    if char not in map :
        map[char] = len(map) % len(color_palette)

    return color_palette[map[char]]

# Fungsi untuk menyimpan gambar
def save_image(board: list[list[str]], queens: list[tuple[int,int]], filename: str, cell_size: int=60):
    n = len(board)
    img_size = n*cell_size
    img = Image.new('RGB', (img_size, img_size), color="#000000")
    draw = ImageDraw.Draw(img)
    color_map = {}

    for i in range (n) :
        for j in range (n) :
            x1 = j*cell_size
            y1 = i*cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            cell_color = get_color(board[i][j], color_map)
            draw.rectangle([x1, y1, x2, y2], fill=cell_color, outline='#34495E', width=2)

    font = ImageFont.truetype("seguisym.ttf", int(cell_size * 0.5))
    for qr, qc in queens : 
        x = qc*cell_size + cell_size//2
        y = qr*cell_size + cell_size//2

        crown = '♕'

        draw.text((x+2, y+2), crown, fill="#FFFEFE", font=font, anchor="mm" )
        draw.text((x, y), crown, fill="#000000", font=font, anchor="mm")
        
    try:
        img.save(filename, 'PNG')
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

# Class untuk bonus GUI
class GUI : 
    def __init__(self, board: list[list[str]], solver_call: callable):
        self.board = board
        self.n = len(board)
        self.solver_call = solver_call
        self.cell_size = min(60, 600//self.n)

        self.root = tk.Tk()
        self.root.title("Brute Force Algorithm for Queens Linkedin Problem")
        self.root.configure(bg='#2C3E50')

        self.color_map = {}
        self.canvas_frame = tk.Frame(self.root, bg='#2C3E50')
        self.canvas_frame.pack(pady=20)
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=self.n*self.cell_size, 
            height=self.n*self.cell_size, 
            bg='#34495E', 
            highlightthickness=0)
        self.canvas.pack()

        self.info_frame = tk.Frame(self.root, bg='#2C3E50')
        self.info_frame.pack(pady=10)

        self.iteration_label = tk.Label(
            self.info_frame, 
            text="Iteration: 0", 
            font=('Arial', 14, 'bold'), 
            bg='#2C3E50', 
            fg='#ECF0F1')
        self.iteration_label.pack()

        self.time_label = tk.Label(
            self.info_frame,
            text="Time: 0 ms",
            font=('Arial', 12),
            bg='#2C3E50',
            fg='#BDC3C7'
        )
        self.time_label.pack()

        self.button_frame = tk.Frame(self.root, bg='#2C3E50')
        self.button_frame.pack(pady=10)

        self.solve_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.start_solving,
            font=('Arial', 12, 'bold'),
            bg='#27AE60',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.save_image_button = tk.Button(
            self.button_frame,
            text="Save Image",
            command=self.save_as_image,
            font=('Arial', 12),
            bg='#3498DB',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.save_image_button.pack(side=tk.LEFT, padx=5)

        self.save_text_button = tk.Button(
            self.button_frame,
            text="Save Text",
            command=self.save_as_text,
            font=('Arial', 12),
            bg='#E67E22',
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.save_text_button.pack(side=tk.LEFT, padx=5)

        self.queens = []
        self.solution = None
        self.execution_time = 0
        self.draw_board()

    def draw_board(self, queens: list[tuple[int,int]]=None) :
        self.canvas.delete('all')

        for i in range (self.n) :
            for j in range (self.n) :
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell_color = get_color(self.board[i][j], self.color_map)
                self.canvas.create_rectangle(
                    x1,y1,x2,y2,
                    fill=cell_color,
                    outline='#34495E',
                    width=2
                )
        if queens :
            for qr, qc in queens :
                x = qc * self.cell_size + self.cell_size // 2
                y = qr * self.cell_size + self.cell_size // 2

                self.canvas.create_text(
                    x, y,
                    text="♕",
                    font=('Arial', int(self.cell_size * 0.6)),
                    fill="#000000"
                )

        self.canvas.update()

    def visualization_call(self, placed_queens: list[tuple[int,int]], iterations: int) :
        self.draw_board(placed_queens)
        self.iteration_label.config(text=f"Iteration: {iterations}")
        self.root.update()

    def start_solving(self) :
        self.solve_button.config(state=tk.DISABLED)
        self.iteration_label.config(text="Searching for a solution ...")
        self.time_label.config(text="Time: 0 ms")

        success, solution, iterations, exec_time, self.queens = self.solver_call(self.visualization_call)

        self.solution = solution
        self.execution_time = exec_time

        if success:
            self.draw_board(self.queens)
            
            self.iteration_label.config(text=f"Solution Found! Iteration: {iterations}")
            self.time_label.config(text=f"Time: {exec_time:.2f} ms")
            
            self.save_image_button.config(state=tk.NORMAL)
            self.save_text_button.config(state=tk.NORMAL)
            
            messagebox.showinfo(
                "Success",
                f"Solution Found!\n\nIteration: {iterations}\nTime: {exec_time:.2f} ms"
            )
        else:
            self.iteration_label.config(text=f"No Solution. Iteration: {iterations}")
            self.time_label.config(text=f"Time: {exec_time:.2f} ms")
            messagebox.showwarning(
                "No Solution",
                f"There is no valid solution for this board.\n\nIteration: {iterations}\nTime: {exec_time:.2f} ms"
            )
        
        self.solve_button.config(state=tk.NORMAL)
    
    def save_as_image(self) :
        if not self.queens:
            messagebox.showwarning("Warning", "There is no solution to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")]
        )
        
        if filename:
            try :
                save_image(self.board, self.queens, filename, cell_size=80)
                messagebox.showinfo("Success", f"Image saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def save_as_text(self):
        if not self.solution:
            messagebox.showwarning("Warning", "There is no solution to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                save_text(self.solution, filename)
                messagebox.showinfo("Success", f"Solution saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def run(self):
        self.root.mainloop()


        
