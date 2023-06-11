import { debounce } from "lodash-es"
import { effect } from "@preact/signals"

import { createAppEffects } from "snd-client/effects/create-effects"
import { OpStatus } from "snd-client/utils"

const PROMPT_DEBOUNCE_MS = 1000

export const createPersonalRecommendationsEffects = createAppEffects(
  (ctx, { cancelAll }) => {
    const {
      state: {
        trackSearch: { searchTerm, searchMode },
        recommendations: { recommendationsState },
      },
      services: { soundationsApi },
    } = ctx

    const subscribe = () => {
      const handleSearchTermChange = debounce(
        async (searchTermValue: string) => {
          if (searchTermValue === "" || searchMode.value !== "prompt") {
            return
          }

          recommendationsState.value = {
            ...recommendationsState.peek(),
            status: OpStatus.LOADING,
          }

          try {
            const response =
              await soundationsApi.tracks.getPersonalRecommendations({
                prompt: searchTermValue,
                limit: 7,
              })

            recommendationsState.value = {
              status: OpStatus.OK,
              result: response.items,
            }
          } catch (error) {
            recommendationsState.value = { status: OpStatus.ERROR, error }
          }
        },
        PROMPT_DEBOUNCE_MS
      )

      return cancelAll([effect(() => handleSearchTermChange(searchTerm.value))])
    }

    return {
      subscribe,
    }
  }
)
