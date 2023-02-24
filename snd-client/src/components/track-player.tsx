import { FunctionalComponent } from "preact"
import { useEffect } from "preact/hooks"

import { useAppContext } from "snd-client/app-context"
import { match } from "snd-client/utils"
import {
  IconPause,
  IconPlay,
  IconSpinner,
  IconVolume,
  IconVolumeMute,
} from "snd-client/components/icons"

export const TrackPlayer: FunctionalComponent = () => {
  const {
    state: {
      trackPlayer: { state, track, volume },
    },
    effects,
  } = useAppContext()

  if (track.value === null) {
    return null
  }

  useEffect(() => {
    return effects.trackPlayer.subscribe()
  }, [])

  const handlePlayClick = () => {
    match(({ assertNever }) => {
      switch (state.value) {
        case "loading":
          break
        case "paused":
          effects.trackPlayer.resume()
          break
        case "playing":
          effects.trackPlayer.pause()
          break
        default:
          return assertNever(state.value)
      }
    })
  }

  const handleVolumeChange = (event: Event) => {
    if (event.target instanceof HTMLInputElement) {
      effects.trackPlayer.setVolume(Number(event.target.value))
    }
  }

  return (
    <div className="w-[80vw] max-w-2xl h-16 fixed bottom-1 left-[50%] translate-x-[-50%] translate-y-[-50%] bg-color-secondary-lessish flex justify-between rounded-md border-2 border-color-primary">
      <div
        role="button"
        tabIndex={0}
        onClick={handlePlayClick}
        className="w-12 ml-4 h-full flex justify-center items-center flex-none"
      >
        <div className="w-12 h-12 flex-none">
          <TrackPlayerIcon state={state.value} />
        </div>
      </div>

      <div className="h-full flex-1 ml-4 mr-4 flex items-center">
        <div className="mr-4 w-12 h-12 aspect-square rounded-md border-solid border-2 border-color-primary">
          <img
            src={track.value?.album.images.at(-1)?.url}
            className="w-full h-full"
          />
        </div>

        <div>
          <div className="font-bold text-sm mb-1">
            {track.value.artists[0]?.name} - {track.value.name}
          </div>
          <div className="text-xs">
            {track.value.album.name} (
            {new Date(track.value.album.release_date).getUTCFullYear()})
          </div>
        </div>
      </div>

      <div className="h-full mr-4 flex flex-none items-center justify-between">
        <IconVolumeMute className="w-8 h-8 mr-2 flex-none fill-current stroke-color-primary text-color-active" />
        <input
          type="range"
          class="h-2 rounded-md flex-1 accent-color-active"
          value={volume}
          onChange={handleVolumeChange}
          min="0"
          max="1"
          step="0.1"
        />
        <IconVolume className="w-8 h-8 ml-2 flex-none fill-current stroke-color-primary text-color-active" />
      </div>
    </div>
  )
}

export const TrackPlayerIcon: FunctionalComponent<{
  state: "loading" | "paused" | "playing"
}> = ({ state }) => {
  const Icon = match(({ assertNever }) => {
    switch (state) {
      case "loading":
        return IconSpinner
      case "paused":
        return IconPlay
      case "playing":
        return IconPause
      default:
        return assertNever(state)
    }
  })

  return (
    <Icon className="w-full h-full fill-current stroke-color-primary text-color-active" />
  )
}
