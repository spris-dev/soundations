import { batch } from "@preact/signals"

import { SoundationsTrack } from "snd-server-api-client"

import { createAppEffects } from "snd-client/effects/create-effects"
import { OpStatus } from "snd-client/utils"

export const createTrackRecommendationsEffects = createAppEffects((ctx) => {
  const {
    state: {
      selectedTrack,
      trackSearch: { searchState },
    },
  } = ctx

  const setSelectedTrack = (track: SoundationsTrack) => {
    console.log(track)

    batch(() => {
      selectedTrack.value = track
      searchState.value = { status: OpStatus.IDLE }
    })
  }

  const subscribe = () => {
    return () => ({})
  }

  return {
    subscribe,
    setSelectedTrack,
  }
})
