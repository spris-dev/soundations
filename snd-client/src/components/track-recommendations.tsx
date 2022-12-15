import { FunctionalComponent } from "preact"
import { useEffect, useRef } from "preact/hooks"
import { useSignal } from "@preact/signals"

import { TrackRecommendationsItem } from "snd-server-api-client"

import { useAppContext } from "snd-client/app-context"
import { OpStatus, rndr } from "snd-client/utils"
import { IconPause, IconPlay } from "snd-client/components/icons"

export const TrackRecommendations: FunctionalComponent = () => {
  const {
    state: {
      selectedTrack: { value: track },
      recommendations: {
        recommendationsState: { value },
      },
    },
    effects,
  } = useAppContext()

  useEffect(() => {
    return effects.trackRecommendations.subscribe()
  }, [])

  return (
    <div className="w-full h-full relative">
      {track && (
        <div className="text-lg mb-2">
          Recommendations for{" "}
          <span className="font-bold">
            {track.artists[0]?.name} - {track.name}
          </span>
          :
        </div>
      )}
      {rndr(({ assertNever }) => {
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
  const isFocused = useSignal(false)
  const trackUrl = `https://open.spotify.com/track/${track.id}`

  return (
    <a
      href={trackUrl}
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
        {track.preview_url && isFocused.value && (
          <div className="w-full h-full bg-color-background opacity-50 absolute top-0 left-0"></div>
        )}
        {track.preview_url && isFocused.value && (
          <div class="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]">
            <TrackAudioPreview mediaUrl={track.preview_url} />
          </div>
        )}
      </div>

      <div>
        <div className="font-bold text-xl">
          {track.artists[0]?.name} - {track.name}
        </div>
        <div>
          {track.album.name} (
          {new Date(track.album.release_date).getUTCFullYear()})
        </div>
        <div className="mt-2 text-lg font-bold italic">
          Similarity:{" "}
          <span className="text-2xl">
            {((recommendation.similarity * 10000) >>> 0) / 100}%
          </span>
        </div>
      </div>
    </a>
  )
}

const TrackAudioPreview: FunctionalComponent<{
  mediaUrl: string
}> = ({ mediaUrl }) => {
  const isPlaying = useSignal(false)
  const audio = useRef<HTMLAudioElement | null>(null)

  useEffect(() => {
    audio.current = new Audio(mediaUrl)
    audio.current.volume = 0.5

    return () => {
      audio.current?.pause()
    }
  }, [mediaUrl])

  const togglePlay = (event: Event) => {
    event.preventDefault()

    if (isPlaying.value) {
      isPlaying.value = false
      audio.current?.pause()
    } else if (
      [
        HTMLMediaElement.HAVE_FUTURE_DATA,
        HTMLMediaElement.HAVE_ENOUGH_DATA,
      ].includes(audio.current?.readyState ?? -1)
    ) {
      isPlaying.value = true
      audio.current?.play()
    }
  }

  const iconClass =
    "w-full h-full fill-current stroke-color-primary text-color-active"

  return (
    <div role="button" onClick={togglePlay} className="w-12 h-12">
      {isPlaying.value ? (
        <IconPause className={iconClass} />
      ) : (
        <IconPlay className={iconClass} />
      )}
    </div>
  )
}
