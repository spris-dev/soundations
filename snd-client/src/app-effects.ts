import type { AppContext } from "snd-client/app-context"
import {
  createTrackSearchEffects,
  createTrackRecommendationsEffects,
  createTrackPlayerEffects,
  createDialogEffects,
  createUserEffects,
} from "snd-client/effects"

type CreateAppEffects = (ctx: AppContext) => {
  trackSearch: ReturnType<typeof createTrackSearchEffects>
  trackRecommendations: ReturnType<typeof createTrackRecommendationsEffects>
  trackPlayer: ReturnType<typeof createTrackPlayerEffects>
  dialog: ReturnType<typeof createDialogEffects>
  user: ReturnType<typeof createUserEffects>
}

export const createAppEffects: CreateAppEffects = (ctx) => {
  return {
    trackSearch: createTrackSearchEffects(ctx),
    trackRecommendations: createTrackRecommendationsEffects(ctx),
    trackPlayer: createTrackPlayerEffects(ctx),
    dialog: createDialogEffects(ctx),
    user: createUserEffects(ctx),
  }
}
