import type { AppContext } from "snd-client/app-context"
import {
  createTrackSearchEffects,
  createTrackRecommendationsEffects,
} from "snd-client/effects"

type CreateAppEffects = (ctx: AppContext) => {
  trackSearch: ReturnType<typeof createTrackSearchEffects>
  trackRecommendations: ReturnType<typeof createTrackRecommendationsEffects>
}

export const createAppEffects: CreateAppEffects = (ctx) => {
  return {
    trackSearch: createTrackSearchEffects(ctx),
    trackRecommendations: createTrackRecommendationsEffects(ctx),
  }
}
