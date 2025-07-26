import { useState, useEffect, useRef, useCallback, useMemo } from "react";
import { getTimeDiff } from "../utils";

const useTimer = () => {
  const timerInterval = useRef<null | number>(null);
  const [timeStarted, setTimeStarted] = useState<Date | null>(null);
  const [timeNow, setTimeNow] = useState<Date | null>(null);
  const timeDiff = useMemo(() => getTimeDiff(timeNow, timeStarted), [timeNow]);
  const isTimerRunning = Boolean(timeStarted);

  const startTimer = useCallback(() => {
    setTimeStarted(new Date());
  }, []);

  const stopTimer = useCallback(() => {
    clearInterval(timerInterval.current!);
  }, []);

  const resetTimer = useCallback(() => {
    setTimeStarted(null);
    setTimeNow(null);
  }, []);

  useEffect(() => {
    if (!timeStarted) return;

    timerInterval.current = setInterval(() => {
      setTimeNow(new Date());
    }, 1000);

    return () => clearInterval(timerInterval.current!);
  }, [timeStarted]);

  return {
    timeDiff,
    isTimerRunning,
    startTimer,
    stopTimer,
    resetTimer,
  };
};

export default useTimer;
