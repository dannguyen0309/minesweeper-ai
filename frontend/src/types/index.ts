import { LEVELS } from "../constants";

type OpenedCell = {
  isOpened: true;
  isFlagged: false;
};

type ClosedCell = {
  isOpened: false;
  isFlagged: boolean;
};

type MineCell = {
  value: "mine";
  highlight?: "red" | "green";
};

type NumberCell = {
  value: number;
};

export type OpenedMineCell = OpenedCell & MineCell;
type ClosedMineCell = ClosedCell & MineCell;
export type OpenedNumberCell = OpenedCell & NumberCell;
type ClosedNumberCell = ClosedCell & NumberCell;

type EmptyCell = {
  value: null;
  isFlagged: false;
  isOpened: false;
};

export type GameCell =
  | OpenedMineCell
  | ClosedMineCell
  | OpenedNumberCell
  | ClosedNumberCell
  | EmptyCell;

export type TBoard = GameCell[][];
export type TLevel = keyof typeof LEVELS;
