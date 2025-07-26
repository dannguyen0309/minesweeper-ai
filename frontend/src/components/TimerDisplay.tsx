import TimerIcon from "/icons/timer.svg";

const TimerDisplay = ({ timeDiff }: { timeDiff: string }) => {
  return (
    <>
      <img src={TimerIcon} className="header-icon" />
      {timeDiff}
    </>
  );
};

export default TimerDisplay;
