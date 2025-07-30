import { GameCell, TBoard } from "../types";
import { DIRECTIONS } from "../constants";

const createBoard = (rows: number, cols: number) => {
  const board: TBoard = [];

  for (let rowIndex = 0; rowIndex < rows; rowIndex++) {
    board[rowIndex] = [];

    for (let cellIndex = 0; cellIndex < cols; cellIndex++) {
      board[rowIndex][cellIndex] = {
        value: null,
        isFlagged: false,
        isOpened: false,
      };
    }
  }

  return board;
};

const fillBoardWithMines = (
  board: TBoard,
  rows: number,
  cols: number,
  totalMines: number
) => {
  let mines = 0;

  while (mines < totalMines) {
    const row = Math.floor(Math.random() * rows);
    const column = Math.floor(Math.random() * cols);

    if (board[row][column].value !== "mine") {
      (board[row][column] as GameCell).value = "mine";
      mines++;
    }
  }

  return board;
};

const fillBoardWithNumbers = (board: TBoard) => {
  // const finalBoard: TBoard = JSON.parse(JSON.stringify(boardWithMines));

  board.forEach((row, rowIndex) => {
    row.forEach((cell, colIndex) => {
      if (cell.value !== "mine") {
        let minesAround = 0;

        DIRECTIONS.forEach(([dRow, dCol]) => {
          const newRow = rowIndex + dRow;
          const newCol = colIndex + dCol;

          if (newRow in board && newCol in board[newRow]) {
            if (board[newRow][newCol].value === "mine") {
              minesAround++;
            }
          }
        });

        cell.value = minesAround;
      }
    });
  });

  return board;
};

export const initBoard = (rows: number, cols: number, totalMines: number) => {
  const emptyBoard = createBoard(rows, cols);
  const boardWithMines = fillBoardWithMines(emptyBoard, rows, cols, totalMines);
  const gameBoard = fillBoardWithNumbers(boardWithMines);

  return gameBoard;
};

export const initGame = (rows: number, cols: number, totalMines: number) => {
  // const boardInStorage = localStorage.getItem(LOCAL_STORAGE_KEYS.gameBoard);
  // console.log("boardInStorage: ", boardInStorage);

  // if (boardInStorage) {
  //   return JSON.parse(boardInStorage) as TBoard;
  // }

  return initBoard(rows, cols, totalMines);
};

export const revealEmptyCells = (
  board: TBoard,
  rows: number,
  cols: number,
  row: number,
  col: number
) => {
  const queue: [number, number][] = [[row, col]]; // Queue of cell coordinates

  while (queue.length > 0) {
    const [currentRow, currentCol] = queue.shift()!; // Dequeue the next cell

    const cell = board[currentRow][currentCol];
    cell.isOpened = true;

    if (cell.value === 0) {
      for (const [dRow, dCol] of DIRECTIONS) {
        const newRow = currentRow + dRow;
        const newCol = currentCol + dCol;

        if (
          newRow >= 0 &&
          newRow < rows &&
          newCol >= 0 &&
          newCol < cols &&
          !board[newRow][newCol].isOpened &&
          !board[newRow][newCol].isFlagged
        ) {
          queue.push([newRow, newCol]); // Add adjacent empty cells to queue
        }
      }
    }
  }

  return board;
};

export const revealAllMines = (board: TBoard, highlightWin?: boolean) => {
  board.forEach((row) => {
    row.forEach((cell) => {
      if (cell.value === "mine") {
        cell.isOpened = true;
        if (highlightWin) {
          cell.highlight = "green";
        }
      }
    });
  });
};

export const checkGameWin = (board: TBoard, totalMines: number) => {
  let unopenedCells = 0;
  let correctlyFlaggedMines = 0;

  board.forEach((row) => {
    row.forEach((cell) => {
      if (!cell.isOpened) {
        unopenedCells++;
      }

      if (cell.isFlagged && cell.value === "mine") {
        correctlyFlaggedMines++;
      }
    });
  });

  // Win condition: All non-mine cells are opened, or all mines are flagged.
  return unopenedCells === totalMines || correctlyFlaggedMines === totalMines;
};

export const getTimeDiff = (timeNow: Date | null, timeStarted: Date | null) => {
  if (timeNow === null || timeStarted === null) return "00:00";
  const diff = Math.floor((timeNow.getTime() - timeStarted.getTime()) / 1000);
  const minutes = Math.floor(diff / 60);
  const seconds = diff % 60;
  return `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;
};
