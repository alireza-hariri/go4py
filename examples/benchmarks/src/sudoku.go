package main

import "C"

import "fmt"

//export SolveSudoku
func SolveSudoku(board_flat []int, print bool) bool {
	board := make([][]int, 9)
	for i := range 9 {
		board[i] = board_flat[i*9 : (i+1)*9]
	}
	return solveSudoku(board, print)
}

func solveSudoku(board [][]int, print bool) bool {

	empty := findEmpty(board)
	if empty == nil {
		return true
	}
	row, col := empty[0], empty[1]
	for i := 1; i <= 9; i++ {
		if valid(board, i, row, col) {
			board[row][col] = i
			if solveSudoku(board, false) {
				if print {
					printBoard(board)
				}
				return true
			}
			board[row][col] = 0
		}
	}

	return false
}

func valid(board [][]int, num, row, col int) bool {
	for i := 0; i < len(board[0]); i++ {
		if board[row][i] == num && col != i {
			return false
		}
	}
	for i := 0; i < len(board); i++ {
		if board[i][col] == num && row != i {
			return false
		}
	}
	boxX := col / 3
	boxY := row / 3
	for i := boxY * 3; i < boxY*3+3; i++ {
		for j := boxX * 3; j < boxX*3+3; j++ {
			if board[i][j] == num && (i != row || j != col) {
				return false
			}
		}
	}
	return true
}

func findEmpty(board [][]int) []int {
	for i := 0; i < len(board); i++ {
		for j := 0; j < len(board[0]); j++ {
			if board[i][j] == 0 {
				return []int{i, j}
			}
		}
	}
	return nil
}

func printBoard(board [][]int) {
	for i := 0; i < len(board); i++ {
		if i%3 == 0 && i != 0 {
			fmt.Println("-----------------------")
		}
		for j := 0; j < len(board[0]); j++ {
			if j%3 == 0 && j != 0 {
				fmt.Print(" | ")
			}
			if j == 8 {
				fmt.Println(board[i][j])
			} else {
				fmt.Print(board[i][j], " ")
			}
		}
	}
}

// func main() {
// 	board := [][]int{
// 		{7, 8, 0, 4, 0, 0, 1, 2, 0},
// 		{6, 0, 0, 0, 7, 5, 0, 0, 9},
// 		{0, 0, 0, 6, 0, 1, 0, 7, 8},
// 		{0, 0, 7, 0, 4, 0, 2, 6, 0},
// 		{0, 0, 1, 0, 5, 0, 9, 3, 0},
// 		{9, 0, 4, 0, 6, 0, 0, 0, 5},
// 		{0, 7, 0, 3, 0, 0, 0, 1, 2},
// 		{1, 2, 0, 0, 0, 7, 4, 0, 0},
// 		{0, 4, 9, 2, 0, 6, 0, 0, 7},
// 	}
// 	if solveSudoku(board) {
// 		for _, row := range board {
// 			fmt.Println(row)
// 		}
// 	} else {
// 		fmt.Println("No solution exists")
// 	}
// }

//
