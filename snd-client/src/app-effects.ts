import type { AppContext } from "snd-client/app-context"
import {
  createTrackSearchEffects,
  createTrackRecommendationsEffects,
  createTrackPlayerEffects,
} from "snd-client/effects"

type CreateAppEffects = (ctx: AppContext) => {
  trackSearch: ReturnType<typeof createTrackSearchEffects>
  trackRecommendations: ReturnType<typeof createTrackRecommendationsEffects>
  trackPlayer: ReturnType<typeof createTrackPlayerEffects>
}

export const createAppEffects: CreateAppEffects = (ctx) => {
  return {
    trackSearch: createTrackSearchEffects(ctx),
    trackRecommendations: createTrackRecommendationsEffects(ctx),
    trackPlayer: createTrackPlayerEffects(ctx),
  }
}
