import { memo } from "react";
import BombIcon from "/icons/bomb.svg";

type Props = {
  isGameWin: boolean;
  isGameOver: boolean;
  isGameEnded: boolean;
  minesLeft: number;
};

const GameStatus = memo((props: Props) => {
  const { isGameWin, isGameOver, isGameEnded, minesLeft } = props;

  return (
    <>
      {isGameWin && <span className="win">You win!</span>}
      {isGameOver && <span className="game-over">Game over!</span>}
      {!isGameEnded && (
        <>
          <img src={BombIcon} className="header-icon" />
          {minesLeft}
        </>
      )}
    </>
  );
});

export default GameStatus;
