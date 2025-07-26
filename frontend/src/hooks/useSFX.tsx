import { useCallback, useEffect, useState } from "react";

const SOUNDS_LIST = {
  REVEAL_EMPTY: "reveal_empty.wav",
  REVEAL_NUMBER: "reveal_number.wav",
  FLAG_PLACE: "flag_place.wav",
  FLAG_REMOVE: "flag_remove.wav",
  GAME_OVER: "game_over.wav",
  GAME_WIN: "game_win.wav",
};

type TSoundName = keyof typeof SOUNDS_LIST;
type TSoundsList = Record<TSoundName, HTMLAudioElement>;

const useSFX = () => {
  const [soundsList, setSoundsList] = useState<TSoundsList | null>(null);

  useEffect(() => {
    if (!soundsList) {
      const list = {} as TSoundsList;

      let sound: TSoundName;
      for (sound in SOUNDS_LIST) {
        list[sound] = new Audio(
          import.meta.env.BASE_URL + "sfx/" + SOUNDS_LIST[sound]
        );
      }

      for (sound in SOUNDS_LIST) {
        list[sound].load();
      }

      setSoundsList(list);
    }
  }, [soundsList]);

  const playSoundEffect = useCallback(
    (sfxName: TSoundName) => {
      try {
        const audioElement = soundsList![sfxName];
        // if (audioElement.HAVE_ENOUGH_DATA) {
        audioElement.pause();
        audioElement.currentTime = 0;
        audioElement.play();
        // }
      } catch (error) {
        console.warn("Unable to play sound: ", error);
      }
    },
    [soundsList]
  );

  return { playSoundEffect };
};

export default useSFX;
