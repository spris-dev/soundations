import { signal, Signal } from "@preact/signals"
import { SoundationsTrack } from "snd-server-api-client"

import { OpStatus } from "snd-client/utils"

export type AppState = {
  trackSearch: {
    searchTerm: Signal<string>
    searchState: Signal<TrackSearchState>
  }
  selectedTrack: Signal<SoundationsTrack | null>
}

type TrackSearchState =
  | { status: OpStatus.IDLE }
  | { status: OpStatus.LOADING; result?: SoundationsTrack[] | null }
  | { status: OpStatus.OK; result: SoundationsTrack[] }
  | { status: OpStatus.ERROR; error: unknown }

type CreateAppState = () => AppState
export const createAppState: CreateAppState = () => {
  return {
    trackSearch: {
      searchTerm: signal(""),
      searchState: signal({ status: OpStatus.IDLE }),
    },
    selectedTrack: signal(null),
  }
}
