import { batch, effect } from "@preact/signals"

import { createAppEffects } from "snd-client/effects/create-effects"
import { UnwrapSignal, wait } from "snd-client/utils"

export const createTrackPlayerEffects = createAppEffects(
  (ctx, { cancelAll }) => {
    const {
      state: {
        trackPlayer: { state, track, volume },
      },
    } = ctx

    const play = (value: UnwrapSignal<typeof track>) => {
      batch(() => {
        track.value = value
        state.value = "loading"
      })
    }

    const pause = () => {
      state.value = "paused"
    }

    const resume = () => {
      state.value = "playing"
    }

    const setVolume = (value: number) => {
      volume.value = value
    }

    const subscribe = () => {
      const audio = new Audio()

      const handleCanPlayThrough = async () => {
        await wait(200)

        audio.play()
        state.value = "playing"
      }

      const handleEnded = () => {
        state.value = "paused"
      }

      return cancelAll([
        effect(() => {
          audio.volume = volume.value
        }),

        effect(() => {
          if (track.value) {
            audio.pause()
            audio.src = track.value.preview_url

            audio.removeEventListener("canplaythrough", handleCanPlayThrough)
            audio.addEventListener("canplaythrough", handleCanPlayThrough)
            audio.removeEventListener("ended", handleEnded)
            audio.addEventListener("ended", handleEnded)
          }
        }),

        effect(() => {
          if (state.value === "playing" && audio.paused) {
            audio.play()
          } else if (state.value === "paused") {
            audio.pause()
          }
        }),
      ])
    }

    return {
      subscribe,
      play,
      pause,
      resume,
      setVolume,
    }
  }
)
