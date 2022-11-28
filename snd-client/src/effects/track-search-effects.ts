import { effect } from "@preact/signals"

import { createAppEffects } from "snd-client/effects/create-effects"
import { OpStatus } from "snd-client/utils"

export const createTrackSearchEffects = createAppEffects((ctx) => {
  const {
    state: {
      trackSearch: { searchTerm, searchState },
    },
    services: { soundationsApi },
  } = ctx

  const setSearchTerm = (value: string) => {
    searchTerm.value = value
  }

  const subscribe = () => {
    return effect(async () => {
      if (searchTerm.value === "") {
        searchState.value = { status: OpStatus.IDLE }
        return
      }

      searchState.value = { ...searchState.peek(), status: OpStatus.LOADING }

      try {
        const response = await soundationsApi.tracks.getTracks({
          q: searchTerm.value,
          limit: 5,
        })

        searchState.value = { status: OpStatus.OK, result: response.items }
      } catch (error) {
        searchState.value = { status: OpStatus.ERROR, error }
      }
    })
  }

  return {
    subscribe,
    setSearchTerm,
  }
})
