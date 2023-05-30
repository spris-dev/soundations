import type { AppContext } from "snd-client/app-context"
import {
  createSoundationsApi,
  createStorage,
  createAuthStateStorage,
} from "snd-client/services"

type CreateAppServices = (ctx: AppContext) => {
  soundationsApi: ReturnType<typeof createSoundationsApi>
  storage: ReturnType<typeof createStorage>
  authStateStorage: ReturnType<typeof createAuthStateStorage>
}

export const createAppServices: CreateAppServices = (ctx) => {
  return {
    soundationsApi: createSoundationsApi(ctx),
    storage: createStorage(ctx),
    authStateStorage: createAuthStateStorage(ctx),
  }
}
