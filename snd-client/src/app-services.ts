import type { AppContext } from "snd-client/app-context"
import { createSoundationsApi } from "snd-client/services"

type CreateAppServices = (ctx: AppContext) => {
  soundationsApi: ReturnType<typeof createSoundationsApi>
}

export const createAppServices: CreateAppServices = (ctx) => {
  return {
    soundationsApi: createSoundationsApi(ctx),
  }
}
