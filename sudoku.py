import os
from pathlib import Path
from timeit import default_timer as timer   

class Sudoku:

    # grid will contain 81 cells for Sudoku board when loaded
    def __init__(self):
        self.grid = []

    # load game grid from text file in data subfolder
    def LoadGame(self):
        # game3.txt is easy
        # game2.txt is "world's hardest"
        # game1.txt is difficult
        with open(Path(os.getcwd(),'data/game3.txt')) as f:
            row = 0
            for line in f:
                line = line.strip()
                values = line.split(",")
                column = 0
                for value in values:
                    cell = Cell(row, column, value)
                    self.grid.append(cell)
                    column +=1
                row += 1
        print("Original Sudoku Grid")
        self.PrintGrid()

    def Solve(self):
        start = timer()
        result = False
        while not result:
            result = self.Iteration()
        print("Completed Sudoku Grid")
        self.PrintGrid()
        print(f"elapsed: {timer()-start} seconds")

    # find valid value for all cells
    # if valid value not available, backtrack one cell and try a different value
    def Iteration(self):
        previousCell = None
        for cell in self.grid:
            cell.previousCell = previousCell
            if cell.fixed == False:
                if cell.value == "":
                    for tryvalue in range(1, 10):
                        if str(tryvalue) not in cell.failedValue:
                            result = self.CheckValue(cell.row, cell.column, tryvalue) and self.CheckSubGrid(cell.row, cell.column, tryvalue)
                            if result == True:
                                cell.value = str(tryvalue)
                                break
                    if cell.value == "":    # back up 1 cell
                        cell.failedValue = []
                        previousCell = cell.previousCell
                        previousCell.failedValue.append(previousCell.value)
                        previousCell.value = ""
                        return False
                previousCell = cell
        return True

    # get a cell given it's row/column value
    def GetCell(self, row, column):
        for cell in self.grid:
            if cell.row == row and cell.column == column:
                return cell

    # check if a given cell value is valid (doesn't conflict with other values in same row/column)
    def CheckValue(self, row, column, value):
        for checkrow in range(9):
            if checkrow == row:
                for checkcolumn in range(9):
                    cell = self.GetCell(checkrow, checkcolumn)
                    if cell.value != "" and int(cell.value) == value:
                        return False
                break
        for checkcolumn in range(9):
            if checkcolumn == column:
                for checkrow in range(9):
                    cell = self.GetCell(checkrow, checkcolumn)
                    if cell.value != "" and int(cell.value) == value:
                        return False
                break
        return True
    
    # check if a given cell value is valid (doesn't conflict with other values in same subgrid)
    def CheckSubGrid(self, row, column, value):
        minrow = 0
        maxrow = 0
        if row <= 2:
            minrow = 0
            maxrow = 2
        elif row > 2 and row <= 5:
            minrow = 3
            maxrow = 5
        else:
            minrow = 6
            maxrow = 8
        mincol = 0
        maxcol = 0
        if column <= 2:
            mincol = 0
            maxcol = 2
        elif column > 2 and column <= 5:
            mincol = 3
            maxcol = 5
        else:
            mincol = 6
            maxcol = 8
        
        for checkrow in range(minrow,maxrow+1):
            for checkcolumn in range(mincol,maxcol+1):
                cell = self.GetCell(checkrow, checkcolumn)
                if cell.value != "" and int(cell.value) == value:
                    return False
            break
        return True
    
    # display grid for review
    def PrintGrid(self):
        currentRow = 0
        for cell in self.grid:
            if currentRow != cell.row:
                print("")
                currentRow = cell.row
            if cell.value == "":
                print(" ", end ="")
            else:
                print(cell.value, end ="")
        print("")
        print("")


class Cell:
    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value
        self.failedValue = []
        if value == "":
            self.fixed = False
        else:
            self.fixed = True
        self.previousCell = None