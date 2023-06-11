import { flow } from "lodash-es"
import { FunctionalComponent } from "preact"
import { useEffect, useCallback } from "preact/hooks"
import { useSignal } from "@preact/signals"

import {
  SoundationsTrack,
  TrackRecommendationsItem,
} from "snd-server-api-client"

import { isTrackPlayerTrack } from "snd-client/app-state"
import { useAppContext } from "snd-client/app-context"
import { useKeyboard } from "snd-client/hooks"
import { OpStatus, match } from "snd-client/utils"
import { TrackPlayerIcon } from "snd-client/components/track-player"

export const TrackRecommendations: FunctionalComponent = () => {
  const {
    state: {
      selectedTrack,
      recommendations: {
        recommendationsState: { value },
      },
    },
    effects,
  } = useAppContext()

  useEffect(() => {
    return flow([
      effects.trackRecommendations.subscribe,
      effects.personalRecommendations.subscribe,
    ])()
  }, [])

  return (
    <div className="w-full h-full relative">
      {selectedTrack.value && (
        <div className="text-lg mb-2">
          Recommendations for{" "}
          <span className="font-bold">
            {selectedTrack.value.artists[0]?.name} - {selectedTrack.value.name}
          </span>
          :
        </div>
      )}
      {match(({ assertNever }) => {
        switch (value.status) {
          case OpStatus.IDLE:
            return null
          case OpStatus.LOADING:
            return <div>Loading...</div>
          case OpStatus.ERROR:
            return <div>{JSON.stringify(value.error)}</div>
          case OpStatus.OK:
            return value.result.map((v) => <TrackRecommendation value={v} />)
          default:
            return assertNever(value)
        }
      })}
    </div>
  )
}

const TrackRecommendation: FunctionalComponent<{
  value: TrackRecommendationsItem
}> = ({ value: { track, recommendation } }) => {
  const trackUrl = `https://open.spotify.com/track/${track.id}`
  const isFocused = useSignal(false)
  const preview = useAudioPreview(track)

  const handleKeyPress = useCallback(
    (event: KeyboardEvent) => {
      if (
        isFocused.value &&
        (event.code === "Enter" || event.code === "Space")
      ) {
        preview?.togglePlay(event)
      }
    },
    [isFocused.value, preview]
  )

  useKeyboard({ onKeyPress: handleKeyPress })

  return (
    <div
      tabIndex={0}
      role="button"
      onClick={preview?.togglePlay}
      className="flex items-center w-full h-40 p-2 mb-4 rounded-md border-2 border-color-primary focus:outline-none focus:bg-color-active-lessish"
      onMouseOver={(event) => {
        isFocused.value = true
        event.target instanceof HTMLElement && event.target.focus()
      }}
      onMouseLeave={() => {
        isFocused.value = false
      }}
      onFocus={() => {
        isFocused.value = true
      }}
      onBlur={() => {
        isFocused.value = false
      }}
    >
      <div className="relative mr-4 h-full aspect-square rounded-md border-solid border-2 border-color-primary">
        <img src={track.album.images[0]?.url} className="w-full h-full" />
        {preview && isFocused.value && (
          <div className="w-full h-full bg-color-background opacity-50 absolute top-0 left-0"></div>
        )}
        {preview && isFocused.value && (
          <div class="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">
            <div className="w-12 h-12">
              <TrackPlayerIcon
                state={preview.isActiveTrack ? preview.playState : "paused"}
              />
            </div>
          </div>
        )}
      </div>

      <div className="overflow-hidden">
        <div className="font-bold text-xl overflow-hidden text-ellipsis whitespace-nowrap">
          {track.artists[0]?.name} - {track.name}
        </div>
        <div className="overflow-hidden text-ellipsis whitespace-nowrap">
          {track.album.name} (
          {new Date(track.album.release_date).getUTCFullYear()})
        </div>
        <div>
          🔗
          <a
            className="mt-2 underline text-color-active"
            href={trackUrl}
            rel="noopener noreferrer"
          >
            Spotify
          </a>
        </div>
        <div className="mt-2 text-lg font-bold italic">
          Similarity:{" "}
          <span className="text-2xl">
            {((recommendation.similarity * 10000) >>> 0) / 100}%
          </span>
        </div>
      </div>
    </div>
  )
}

const useAudioPreview = (track: SoundationsTrack) => {
  if (!isTrackPlayerTrack(track)) {
    return null
  }

  const {
    state: { trackPlayer },
    effects: {
      trackPlayer: { play, pause, resume },
    },
  } = useAppContext()

  const isActiveTrack = trackPlayer.track.value?.id === track.id
  const playState = trackPlayer.state.value

  const togglePlay = (event: Event) => {
    event.preventDefault()

    if (!isActiveTrack) {
      play(track)
    } else if (playState === "playing") {
      pause()
    } else if (playState === "paused") {
      resume()
    }
  }

  return {
    isActiveTrack,
    playState,
    togglePlay,
  }
}
