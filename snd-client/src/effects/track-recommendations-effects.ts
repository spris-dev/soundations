import { batch, effect } from "@preact/signals"

import { SoundationsTrack } from "snd-server-api-client"

import { createAppEffects } from "snd-client/effects/create-effects"
import { OpStatus } from "snd-client/utils"

export const createTrackRecommendationsEffects = createAppEffects((ctx) => {
  const {
    state: {
      selectedTrack,
      trackSearch: { searchState },
      recommendations: { recommendationsState },
    },
    services: { soundationsApi },
  } = ctx

  const setSelectedTrack = (track: SoundationsTrack) => {
    batch(() => {
      selectedTrack.value = track
      searchState.value = { status: OpStatus.IDLE }
    })
  }

  const subscribe = () => {
    return effect(async () => {
      if (selectedTrack.value === null) {
        recommendationsState.value = { status: OpStatus.IDLE }
        return
      }

      recommendationsState.value = {
        ...recommendationsState.peek(),
        status: OpStatus.LOADING,
      }

      try {
        const response = await soundationsApi.tracks.getTrackRecommendations({
          trackId: selectedTrack.value.id,
          limit: 7,
        })

        recommendationsState.value = {
          status: OpStatus.OK,
          result: response.items,
        }
      } catch (error) {
        recommendationsState.value = { status: OpStatus.ERROR, error }
      }
    })
  }

  return {
    subscribe,
    setSelectedTrack,
  }
})
