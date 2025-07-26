import GameStatus from "./GameStatus";
import TimerDisplay from "./TimerDisplay";

type HeaderProps = {
  isGameWin: boolean;
  isGameOver: boolean;
  isGameEnded: boolean;
  minesLeft: number;
  startNewGame: () => void;
  restartGame: () => void;
  timeDiff: string;
};

const Header = ({
  isGameWin,
  isGameOver,
  isGameEnded,
  minesLeft,
  startNewGame,
  restartGame,
  timeDiff,
}: HeaderProps) => {
  return (
    <header>
      <div className="header-label">
        <GameStatus
          isGameWin={isGameWin}
          isGameOver={isGameOver}
          isGameEnded={isGameEnded}
          minesLeft={minesLeft}
        />
      </div>
      <div className="header-buttons">
        <button onClick={startNewGame}>New</button>
        <button onClick={restartGame}>Restart</button>
      </div>
      <div className="header-label">
        <TimerDisplay timeDiff={timeDiff} />
      </div>
    </header>
  );
};

export default Header;
