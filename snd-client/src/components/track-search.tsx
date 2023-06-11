import { FunctionalComponent } from "preact"
import { useEffect, useRef } from "preact/hooks"
import { useSignal } from "@preact/signals"

import { SoundationsTrack } from "snd-server-api-client"

import { useAppContext } from "snd-client/app-context"
import { IconSearch } from "snd-client/components/icons"
import { Input } from "snd-client/components/input"
import { Button } from "snd-client/components/button"
import { OpStatus, match } from "snd-client/utils"

type TrackSearchProps = Record<never, never>

export const TrackSearch: FunctionalComponent<TrackSearchProps> = () => {
  const { effects } = useAppContext()

  useEffect(() => {
    return effects.trackSearch.subscribe()
  }, [])

  return (
    <div className="w-full h-full relative z-10 bg-color-background">
      <TrackSearchInput />
      <TrackSearchResults />
    </div>
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
      rightNode={<TrackSearchModeToggle />}
      value={searchTerm}
      onChange={effects.trackSearch.setSearchTerm}
      placeholder={placeholder}
    />
  )
}

export const TrackSearchModeToggle: FunctionalComponent = () => {
  const {
    state: {
      trackSearch: { searchMode },
    },
    effects,
  } = useAppContext()

  return (
    <div className="h-11 flex items-center">
      <Button
        variant="secondary"
        onClick={() =>
          effects.trackSearch.setSearchMode(
            searchMode.value === "track" ? "prompt" : "track"
          )
        }
      >
        {searchMode.value === "track" ? "Track Mode" : "Prompt Mode"}
      </Button>
    </div>
  )
}

export const TrackSearchResults: FunctionalComponent = () => {
  const {
    state: {
      trackSearch: {
        searchState: { value: search },
      },
    },
    effects,
  } = useAppContext()

  return (
    <>
      {match(({ assertNever }) => {
        switch (search.status) {
          case OpStatus.IDLE:
            return null
          case OpStatus.LOADING:
            return search.result ? (
              <TrackSearchResultsView
                tracks={search.result}
                onTrackSelect={effects.trackRecommendations.setSelectedTrack}
              />
            ) : (
              <div>Loading...</div>
            )
          case OpStatus.ERROR:
            return <div>{JSON.stringify(search.error)}</div>
          case OpStatus.OK:
            return (
              <TrackSearchResultsView
                tracks={search.result}
                onTrackSelect={effects.trackRecommendations.setSelectedTrack}
              />
            )
          default:
            return assertNever(search)
        }
      })}
    </>
  )
}

export const TrackSearchResultsView: FunctionalComponent<{
  tracks: SoundationsTrack[]
  onTrackSelect: (track: SoundationsTrack) => void
}> = ({ tracks, onTrackSelect }) => {
  return (
    <div className="absolute top-[100%] w-full pt-2 pb-2 shadow-md rounded-md border-2 border-color-primary border-t-0 bg-color-background">
      {tracks.map((track) => (
        <div
          className="flex items-center w-full h-20 p-2 pl-4 pr-4 border-b last:border-b-0 border-color-secondary-lessish focus:outline-none focus:bg-color-active-lessish"
          tabIndex={0}
          role="button"
          onClick={() => onTrackSelect(track)}
          onKeyDown={(event) =>
            ["Enter", " "].includes(event.key) && onTrackSelect(track)
          }
          onMouseOver={(event) => {
            event.target instanceof HTMLElement && event.target.focus()
          }}
        >
          <img
            src={track.album.images[0]?.url}
            className="mr-2 h-full rounded-md border-solid border-2 border-color-primary"
          />
          <div className="">
            <div className="font-bold text-lg">
              {track.artists[0]?.name} - {track.name}
            </div>
            <div>
              {track.album.name} (
              {new Date(track.album.release_date).getUTCFullYear()})
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
