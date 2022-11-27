import type { AppContext } from "snd-client/app-context"
import { createTrackSearchEffects } from "snd-client/effects"

type CreateAppEffects = (ctx: AppContext) => {
  trackSearch: ReturnType<typeof createTrackSearchEffects>
}

export const createAppEffects: CreateAppEffects = (ctx) => {
  return {
    trackSearch: createTrackSearchEffects(ctx),
  }
}
