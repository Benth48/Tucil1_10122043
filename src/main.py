import sys
from solver import board_solver
from utils import read_file, save_text, save_image, GUI
import tkinter as tk
from tkinter import filedialog

# Fungsi untuk print papan
def print_board(board: list[list[str]]):
    for row in board:
        print(''.join(row))

# Fungsi untuk output berupa Command Line Interface (CLI)
def cli_mode():
    print()

    filename = input("Enter the input file name (Example: test1.txt): ").strip()

    try:
        print(f"\nRead the file : '{filename}'...")
        board = read_file(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print(f"\nBoard Size: {len(board)}x{len(board)}")
    print("\nInitial Board:")
    print_board(board)
    print()
    
    input("Press enter to continue...")
    
    solver = board_solver(board)
    
    # Fungsi untuk visualisas CLI
    def cli_visualization(placed_queens, iterations):
        print(f"\nIteration: {iterations}")
        
        temp_board = [row[:] for row in board]
        for qr, qc in placed_queens:
            temp_board[qr][qc] = '#'
        
        for row in temp_board:
            row_str = ""
            for cell in row:
                row_str += cell + " "
            print(row_str)
        
        print()
    
    print("\nSearching for solution...\n")
    success, solution, iterations, exec_time, queens = solver.solve(cli_visualization)
    
    print("Result :")
    print()
    
    if success:
        print("Solution Found!")
        print()
        print_board(solution)
        print()
        print(f"Execution Time: {exec_time:.2f} ms")
        print(f"Cases Reviewed: {iterations} cases")
        print()
        
        save_choice = input("Save the solution as text? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes', 'ya']:
            output_filename = input("Output file name (Example: solution.txt): ").strip()
            try:
                save_text(solution, output_filename)
                print(f"Solution saved successfully to '{output_filename}'")
            except Exception as e:
                print(f"Error saving file: {e}")

        image_choice = input("\nSave the solution as a PNG image? (y/n): ").strip().lower()
        if image_choice in ['y', 'yes', 'ya']:
            image_filename = input("Image file name (Example: solution.png): ").strip()
            try :
                save_image(board, queens, image_filename)
                print(f"Image saved successfully to '{image_filename}'")
            except Exception as e:
                print(f"Error saving file: {e}")
    else:
        print("There is no valid solution for this board")
        print()
        print(f"Execution Time: {exec_time:.2f} ms")
        print(f"Cases Reviewed: {iterations} cases")
    
    print()
    print("Finish.")

# Fungsi untuk output berupa GUI
def run_gui_mode():
    root = tk.Tk()
    root.withdraw() 
    
    filename = filedialog.askopenfilename(
        title="Select Input File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if not filename:
        print("No files selected. Exit the program..")
        return
    
    try:
        board = read_file(filename)
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        from tkinter import messagebox
        messagebox.showerror(f"Error! Failed to read file:\n{e}")
        return
    
    root.destroy() 
    
    solver = board_solver(board)
    
    def solve_visualization(visualization_call):
        return solver.solve(visualization_call)
    
    gui = GUI(board, solve_visualization)
    gui.run()

# Main Code untuk menjalankan
def main():
    print("--- Brute Force Algorithm for Queens Linkedin Problem ---")
    print()
    print("Select mode:")
    print("1. CLI Mode (Command Line Interface)")
    print("2. GUI Mode (Graphical User Interface)")
    print()
    
    choice = input("Your choice (1/2): ").strip()
    
    if choice == '1':
        cli_mode()
    elif choice == '2':
        run_gui_mode()
    else:
        print("Invalid selection!")
        sys.exit(1)


if __name__ == "__main__":
    main()