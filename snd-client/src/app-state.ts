import { signal, Signal } from "@preact/signals"
import {
  SoundationsTrack,
  TrackRecommendationsItem,
} from "snd-server-api-client"

import { OpStatus } from "snd-client/utils"

export type AppState = {
  trackSearch: {
    searchTerm: Signal<string>
    searchState: Signal<TrackSearchState>
  }
  selectedTrack: Signal<SoundationsTrack | null>
  recommendations: {
    recommendationsState: Signal<RecommendationsState>
  }
  trackPlayer: {
    state: Signal<"playing" | "paused" | "loading">
    track: Signal<TrackPlayerTrack | null>
    volume: Signal<number>
  }
}

export type TrackPlayerTrack = SoundationsTrack & {
  preview_url: NonNullable<SoundationsTrack["preview_url"]>
}

type TrackSearchState =
  | { status: OpStatus.IDLE }
  | { status: OpStatus.LOADING; result?: SoundationsTrack[] | null }
  | { status: OpStatus.OK; result: SoundationsTrack[] }
  | { status: OpStatus.ERROR; error: unknown }

type RecommendationsState =
  | { status: OpStatus.IDLE }
  | { status: OpStatus.LOADING }
  | { status: OpStatus.OK; result: TrackRecommendationsItem[] }
  | { status: OpStatus.ERROR; error: unknown }

type CreateAppState = () => AppState
export const createAppState: CreateAppState = () => {
  return {
    trackSearch: {
      searchTerm: signal(""),
      searchState: signal({ status: OpStatus.IDLE }),
    },
    selectedTrack: signal(null),
    recommendations: {
      recommendationsState: signal({ status: OpStatus.IDLE }),
    },
    trackPlayer: {
      state: signal("paused"),
      track: signal(null),
      volume: signal(0.5),
    },
  }
}

export const isTrackPlayerTrack = (
  track: SoundationsTrack
): track is TrackPlayerTrack => track.preview_url != null
