import { debounce } from "lodash-es"
import { effect } from "@preact/signals"

import { createAppEffects } from "snd-client/effects/create-effects"
import { OpStatus, UnwrapSignal } from "snd-client/utils"

const SEARCH_DEBOUNCE_MS = 500

export const createTrackSearchEffects = createAppEffects(
  (ctx, { cancelAll }) => {
    const {
      state: {
        trackSearch: { searchTerm, searchState, searchMode },
        selectedTrack,
        recommendations: { recommendationsState },
      },
      services: { soundationsApi },
    } = ctx

    const setSearchTerm = (value: string) => {
      searchTerm.value = value
    }

    const setSearchMode = (value: UnwrapSignal<typeof searchMode>) => {
      searchMode.value = value
    }

    const subscribe = () => {
      const handleSearchTermChange = debounce(
        async (searchTermValue: string) => {
          if (searchTermValue === "") {
            searchState.value = { status: OpStatus.IDLE }
            recommendationsState.value = { status: OpStatus.IDLE }
            return
          }

          if (searchMode.value !== "track") {
            selectedTrack.value = null
            return
          }

          searchState.value = {
            ...searchState.peek(),
            status: OpStatus.LOADING,
          }

          try {
            const response = await soundationsApi.tracks.getTracks({
              q: searchTermValue,
              limit: 5,
            })

            searchState.value = { status: OpStatus.OK, result: response.items }
          } catch (error) {
            searchState.value = { status: OpStatus.ERROR, error }
          }
        },
        SEARCH_DEBOUNCE_MS
      )

      return cancelAll([effect(() => handleSearchTermChange(searchTerm.value))])
    }

    return {
      subscribe,
      setSearchTerm,
      setSearchMode,
    }
  }
)
