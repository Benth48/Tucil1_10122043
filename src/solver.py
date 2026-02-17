import time 


class board_solver :
    def __init__(self, board:list[list[str]]):
        self.board = board
        self.n = len(board)
        self.solution = [[' ' for i in range(self.n)] for j in range(self.n)]
        self.iterations = 0
        self.start_time = 0
        self.execution_time = 0
        self.regions = self.color_regions()
        self.visualization_call = None
    
    # Mapping setiap warna ke posisi sel nya
    def color_regions(self) :
        regions = {}
        for i in range(self.n) :
            for j in range(self.n) :
                color = self.board[i][j]
                if color not in regions :
                    regions[color] = []
                regions[color].append((i,j))
        return regions
    
    # Cek setiap pasangan bidak apakah bertetangga
    def check_neighbor (self, row1: int, col1: int, row2: int, col2: int) :
        return abs(row1-row2) <= 1 and abs(col1-col2) <= 1 and (row1!=row2 or col1!=col2) 
    
    # Cek apakah posisi bidak valid
    def check_valid(self, row: int, col: int, placed_queens: list[tuple[int,int]]) :
        self.iterations +=1
        current_color = self.board[row][col]
        for qr, qc in placed_queens :
            if qr == row :
                return False
            elif qc == col : 
                return False
            elif self.board[qr][qc] == current_color :
                return False
            elif self.check_neighbor(row,col,qr,qc) :
                return False
        return True
    
    # Pemasangan bidak secara rekursif
    def solver_recursive(self, row: int, placed_queens: list[tuple[int,int]]) :
        if row == self.n :
            return True
        
        for col in range(self.n) :
            if self.check_valid(row, col, placed_queens) :
                placed_queens.append((row,col))

                if self.visualization_call:
                    self.visualization_call(placed_queens, self.iterations)

                if self.solver_recursive(row+1, placed_queens) :
                    return True
                
                placed_queens.pop()
        
        return False
    
    # Fungsi utama untuk Solve
    def solve(self, visualization_call=None) :
        self.iterations = 0
        self.start_time = time.time()
        placed_queens = []
        self.visualization_call = visualization_call
        
        success = self.solver_recursive(0,placed_queens)
        self.execution_time = (time.time() - self.start_time) * 1000

        if success :
            for qr, qc in placed_queens:
                self.solution[qr][qc] = '#'

            for i in range (self.n) :
                for j in range (self.n) :
                    if self.solution[i][j]!='#' :
                        self.solution[i][j] = self.board[i][j]
        
        return success, self.solution, self.iterations, self.execution_time, placed_queens