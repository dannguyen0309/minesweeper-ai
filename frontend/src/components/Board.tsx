import { memo, MouseEvent } from "react";
import { TBoard, TLevel } from "../types";
import Cell from "./Cell";

type BoardProps = {
  gameBoard: TBoard;
  handleCellLeftClick: (row: number, col: number) => void;
  handleCellRightClick: (
    e: MouseEvent<HTMLDivElement>,
    row: number,
    col: number
  ) => void;
  level: TLevel;
};

const Board = memo(
  ({
    gameBoard,
    handleCellLeftClick,
    handleCellRightClick,
    level,
  }: BoardProps) => {
    return (
      <div className="board">
        {gameBoard.map((rows, rowIndex) => (
          <div className="row" key={rowIndex}>
            {rows.map((cell, cellIndex) => (
              <Cell
                cell={cell}
                rowIndex={rowIndex}
                cellIndex={cellIndex}
                handleCellLeftClick={handleCellLeftClick}
                handleCellRightClick={handleCellRightClick}
                level={level}
                key={cellIndex}
              />
            ))}
          </div>
        ))}
      </div>
    );
  }
);

export default Board;
