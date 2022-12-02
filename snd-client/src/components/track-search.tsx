import { FunctionalComponent } from "preact"
import { useEffect, useRef } from "preact/hooks"
import { useSignal } from "@preact/signals"

import { SoundationsTrack } from "snd-server-api-client"

import { useAppContext } from "snd-client/app-context"
import { IconSearch } from "snd-client/components/icons"
import { Input } from "snd-client/components/input"
import { OpStatus, rndr } from "snd-client/utils"

type TrackSearchProps = Record<never, never>

export const TrackSearch: FunctionalComponent<TrackSearchProps> = () => {
  const { effects } = useAppContext()

  useEffect(() => {
    return effects.trackSearch.subscribe()
  }, [])

  return (
    <>
      <TrackSearchInput />
      <TrackSearchResults />
    </>
  )
}

const SONG_PLACEHOLDERS = [
  "More Than I Could Chew - Mastodon",
  "Mission To Mars - Megadeth",
  "Black Rose Immortal - Opeth",
]
const PLACEHOLDER_TYPING_DELAY_MS = 90
const FULL_PLACEHOLDER_STATE_DELAY_MS = 1500

export const TrackSearchInput: FunctionalComponent = () => {
  const {
    state: {
      trackSearch: { searchTerm },
    },
    effects,
  } = useAppContext()

  const placeholder = useSignal(SONG_PLACEHOLDERS[0])
  const currentSongIdx = useRef(0)
  const skipFramesCount = useRef(0)

  useEffect(() => {
    if (searchTerm.value.length > 0) {
      return
    }

    const id = setInterval(() => {
      if (skipFramesCount.current > 0) {
        skipFramesCount.current -= 1

        if (skipFramesCount.current === 0) {
          currentSongIdx.current =
            (currentSongIdx.current + 1) % SONG_PLACEHOLDERS.length
          placeholder.value = ""
        }

        return
      }

      if (
        placeholder.value.length ===
        SONG_PLACEHOLDERS[currentSongIdx.current].length
      ) {
        skipFramesCount.current +=
          (FULL_PLACEHOLDER_STATE_DELAY_MS / PLACEHOLDER_TYPING_DELAY_MS) >>> 0
        return
      }

      placeholder.value = SONG_PLACEHOLDERS[currentSongIdx.current].slice(
        0,
        placeholder.value.length + 1
      )
    }, PLACEHOLDER_TYPING_DELAY_MS)

    return () => {
      clearInterval(id)
    }
  }, [searchTerm.value])

  return (
    <Input
      icon={<IconSearch />}
      value={searchTerm}
      onChange={effects.trackSearch.setSearchTerm}
      placeholder={placeholder}
    />
  )
}

export const TrackSearchResults: FunctionalComponent = () => {
  const {
    state: {
      trackSearch: {
        searchState: { value: search },
      },
    },
  } = useAppContext()

  return (
    <>
      {rndr(({ assertNever }) => {
        switch (search.status) {
          case OpStatus.IDLE:
            return null
          case OpStatus.LOADING:
            return search.result ? (
              <TrackSearchResultsView tracks={search.result} />
            ) : (
              <div>Loading...</div>
            )
          case OpStatus.ERROR:
            return <div>{JSON.stringify(search.error)}</div>
          case OpStatus.OK:
            return <TrackSearchResultsView tracks={search.result} />
          default:
            return assertNever(search)
        }
      })}
    </>
  )
}

export const TrackSearchResultsView: FunctionalComponent<{
  tracks: SoundationsTrack[]
}> = ({ tracks }) => {
  return (
    <div>
      {tracks.map((track) => (
        <div className="flex">
          <img src={track.album.images[0]?.url} className="w-32 h-32 p-8"></img>
          <div className="p-8">
            <div className="font-bold">{track.name}</div>
            <div>
              {track.album.name} - {track.album.release_date}
            </div>
            <div>{track.artists[0]?.name}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
