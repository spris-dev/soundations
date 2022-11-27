import { useEffect, useMemo } from "preact/hooks"
import { debounce } from "lodash-es"

import { createAppContext } from "snd-client/app-context"
import { Layout } from "snd-client/components/layout"
import { OpStatus } from "snd-client/utils"

const SEARCH_DEBOUNCE_MS = 1000

const ctx = createAppContext()

export function App() {
  const {
    state: {
      trackSearch: { searchState },
    },
    effects,
  } = ctx

  useEffect(() => {
    return effects.trackSearch.subscribe()
  }, [])

  const handleSearchInput = (event: Event) => {
    if (event.target instanceof HTMLInputElement) {
      effects.trackSearch.setSearchTerm(event.target.value)
    }
  }

  const handleSearchInputDebounced = useMemo(
    () => debounce(handleSearchInput, SEARCH_DEBOUNCE_MS),
    [handleSearchInput]
  )

  return (
    <Layout>
      <input
        className="p-8 border-2"
        type="text"
        onInput={handleSearchInputDebounced}
      />
      {searchState.value.status === OpStatus.LOADING &&
        !searchState.value.result && <div>Loading...</div>}
      {searchState.value.status === OpStatus.ERROR && (
        <div>{JSON.stringify(searchState.value.error)}</div>
      )}
      {searchState.value.status === OpStatus.OK && (
        <div>
          {searchState.value.result.map((track) => (
            <div className="flex">
              <img
                src={track.album.images[0].url}
                className="w-32 h-32 p-8"
              ></img>
              <div className="p-8">
                <div className="font-bold">{track.name}</div>
                <div>
                  {track.album.name} - {track.album.release_date}
                </div>
                <div>{track.artists[0].name}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  )
}
