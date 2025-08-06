// Core
import { MouseEvent, useCallback, useEffect, useState } from "react";
import useTimer from "./useTimer";
import useSFX from "./useSFX";

// Constants
import { DEFAULT_LEVEL, LEVELS } from "../constants";

// Utils
import {
  checkGameWin,
  initBoard,
  initGame,
  revealAllMines,
  revealEmptyCells,
} from "../utils";

// Types
import type { TBoard, TLevel } from "../types";

const useMinesweeperGame = () => {
  const [level, setLevel] = useState<TLevel>("easy");
  const currentLevel = LEVELS[level];
  const [isAISolving, setIsAISolving] = useState(false);

  const changeLevel = useCallback((selectedLevel: TLevel) => {
    setLevel(selectedLevel);
  }, []);

  const [gameBoard, setGameBoard] = useState<TBoard>(
    initGame(
      LEVELS[DEFAULT_LEVEL].rows,
      LEVELS[DEFAULT_LEVEL].cols,
      LEVELS[DEFAULT_LEVEL].totalMines
    )
  );

  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const [isGameWin, setIsGameWin] = useState(false);
  const [isGameOver, setIsGameOver] = useState(false);
  const isGameEnded = isGameWin || isGameOver;

  const [totalFlags, setTotalFlags] = useState(0);
  const minesLeft = currentLevel.totalMines - totalFlags;

  const { timeDiff, isTimerRunning, startTimer, stopTimer, resetTimer } =
    useTimer();

  const { playSoundEffect } = useSFX();

  const resetBoard = useCallback(
    (isRestart?: boolean) => {
      stopTimer();
      resetTimer();
      setTotalFlags(0);
      setIsGameOver(false);
      setIsGameWin(false);

      if (isRestart) {
        setGameBoard((prevGameBoard) =>
          prevGameBoard.map((row) =>
            row.map((cell) => {
              return {
                value: cell.value,
                isFlagged: false,
                isOpened: false,
              };
            })
          )
        );
      } else {
        setGameBoard(
          initGame(
            currentLevel.rows,
            currentLevel.cols,
            currentLevel.totalMines
          )
        );
      }
    },
    [currentLevel, resetTimer, stopTimer]
  );

  const startNewGame = useCallback(() => {
    resetBoard();
  }, [resetBoard]);

  const restartGame = useCallback(() => {
    resetBoard(true);
  }, [resetBoard]);

  useEffect(() => {
    if (isGameEnded) {
      stopTimer();
    }
  }, [isGameEnded, stopTimer]);

  useEffect(() => {
    startNewGame();
  }, [level, startNewGame]);

  const openCell = useCallback(
    (board: TBoard, row: number, col: number): TBoard | null => {
      const newGameBoard: TBoard = JSON.parse(JSON.stringify(board));
      const cell = newGameBoard[row][col];
      const isMineCell = cell.value === "mine";
      const isNumberCell = typeof cell.value === "number" && cell.value > 0;

      if (isMineCell) {
        cell.highlight = "red";
        setIsGameOver(true);
        playSoundEffect("GAME_OVER");
        revealAllMines(newGameBoard);
      }

      if (!isMineCell) {
        cell.isOpened = true;
        if (cell.value === 0) {
          playSoundEffect("REVEAL_EMPTY");

          revealEmptyCells(
            newGameBoard,
            currentLevel.rows,
            currentLevel.cols,
            row,
            col
          );
        }

        if (isNumberCell) {
          playSoundEffect("REVEAL_NUMBER");
        }

        if (checkGameWin(newGameBoard, currentLevel.totalMines)) {
          revealAllMines(newGameBoard, true);
          setIsGameWin(true);
          playSoundEffect("GAME_WIN");
        }
      }

      return newGameBoard;
    },
    [currentLevel, isTimerRunning, playSoundEffect, startTimer]
  );

  const handleCellLeftClick = useCallback(
    (row: number, col: number) => {
      if (
        isGameEnded ||
        gameBoard[row][col].isOpened ||
        gameBoard[row][col].isFlagged
      ) {
        return null;
      }

      const mineCell = gameBoard[row][col].value === "mine";
      const isFirstClick = !isTimerRunning;
      const isFirstClickOnMine = mineCell && isFirstClick;

      let newGameBoard: TBoard;

      if (isFirstClickOnMine) {
        do {
          newGameBoard = initBoard(
            currentLevel.rows,
            currentLevel.cols,
            currentLevel.totalMines
          );
        } while (newGameBoard[row][col].value === "mine");
      } else {
        newGameBoard = JSON.parse(JSON.stringify(gameBoard));
      }

      const boardAfterOpeningCell = openCell(newGameBoard, row, col);

      if (boardAfterOpeningCell) {
        setGameBoard(boardAfterOpeningCell);
      }
    },
    [isGameEnded, gameBoard, isTimerRunning, openCell, currentLevel]
  );

  const handleCellRightClick = useCallback(
    (e: MouseEvent<HTMLDivElement>, row: number, col: number) => {
      e.preventDefault();

      if (isGameEnded || gameBoard[row][col].isOpened) return;

      if (!isTimerRunning) startTimer();

      let flagsDiff = 0;

      setGameBoard((prevGameBoard) => {
        const newGameBoard: TBoard = JSON.parse(JSON.stringify(prevGameBoard));
        const cell = prevGameBoard[row][col];

        if (cell.isFlagged) {
          newGameBoard[row][col].isFlagged = false;
          if (!flagsDiff) flagsDiff--;
          playSoundEffect("FLAG_REMOVE");
        }

        if (!cell.isFlagged) {
          newGameBoard[row][col].isFlagged = true;
          if (!flagsDiff) flagsDiff++;
          playSoundEffect("FLAG_PLACE");
        }

        if (checkGameWin(newGameBoard, currentLevel.totalMines)) {
          revealAllMines(newGameBoard, true);
          setIsGameWin(true);
          playSoundEffect("GAME_WIN");
        }

        return newGameBoard;
      });

      setTotalFlags((prevTotalFlags) => prevTotalFlags + flagsDiff);
    },
    [
      gameBoard,
      isGameEnded,
      isTimerRunning,
      currentLevel.totalMines,
      playSoundEffect,
      startTimer,
    ]
  );

  return {
    level,
    changeLevel,
    gameBoard,
    minesLeft,
    timeDiff,
    startNewGame,
    restartGame,
    handleCellLeftClick,
    handleCellRightClick,
    isGameWin,
    isGameOver,
    isGameEnded,
    isAISolving,
    aiSolve: async () => {
      if (isGameEnded || isAISolving) return;
      if (!isTimerRunning) startTimer();
      setIsAISolving(true);
      try {
        let board = JSON.parse(JSON.stringify(gameBoard));
        let flags = [];
        for (let r = 0; r < board.length; r++) {
          for (let c = 0; c < board[r].length; c++) {
            if (board[r][c].isFlagged) flags.push(cellId(r, c));
          }
        }
        function cellId(row: number, col: number) {
          // Dynamically support all board sizes
          const rowLabels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            .split("")
            .slice(0, currentLevel.rows);
          return rowLabels[row] + (col + 1);
        }
        function getOpened(board: TBoard) {
          const opened: Record<string, number> = {};
          for (let r = 0; r < board.length; r++) {
            for (let c = 0; c < board[r].length; c++) {
              if (
                board[r][c].isOpened &&
                typeof board[r][c].value === "number"
              ) {
                opened[cellId(r, c)] = board[r][c].value as number;
              }
            }
          }
          return opened;
        }
        function getUnopened(board: TBoard) {
          const unopened: string[] = [];
          for (let r = 0; r < board.length; r++) {
            for (let c = 0; c < board[r].length; c++) {
              if (!board[r][c].isOpened && !board[r][c].isFlagged) {
                unopened.push(cellId(r, c));
              }
            }
          }
          return unopened;
        }
        let keepGoing = true;
        while (keepGoing) {
          const opened = getOpened(board);
          const unopened = getUnopened(board);
          const payload = {
            opened,
            unopened,
            flagged: flags,
            total_mines: currentLevel.totalMines,
          };
          const res = await fetch(`${backendUrl}/play-move`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });
          const { action, cell } = await res.json();
          if (!cell) break;
          // Find cell coordinates
          const rowLabels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            .split("")
            .slice(0, currentLevel.rows);
          const row = rowLabels.indexOf(cell[0]);
          const col = parseInt(cell.slice(1)) - 1;
          if (action === "open") {
            if (!board[row][col].isOpened && !board[row][col].isFlagged) {
              board = openCell(board, row, col) || board;
            }
          } else if (action === "flag") {
            if (!board[row][col].isFlagged && !board[row][col].isOpened) {
              board[row][col].isFlagged = true;
              flags.push(cellId(row, col));
            }
          }
          // End if game is won/lost or no more moves
          if (checkGameWin(board, currentLevel.totalMines)) {
            keepGoing = false;
          }
          if (board[row][col].value === "mine" && action === "open") {
            keepGoing = false;
          }
          // End if no unopened left
          if (getUnopened(board).length === 0) {
            keepGoing = false;
          }
          setGameBoard(board);
          await new Promise((res) => setTimeout(res, 200)); // allow UI/timer to update
        }
        setGameBoard(board);
        // Patch: After loop, check if game is won and update state if needed
        if (checkGameWin(board, currentLevel.totalMines)) {
          setIsGameWin(true);
        }
      } catch (e) {
        // handle error
      }
      setIsAISolving(false);
    },
  };
};

export default useMinesweeperGame;
