import type { AppContext } from "snd-client/app-context"

type AppEffectsResult<T> = T & {
  subscribe: () => () => void
}

type CreateAppEffects = <T>(
  effectsCreator: (ctx: AppContext) => AppEffectsResult<T>
) => (ctx: AppContext) => AppEffectsResult<T>

export const createAppEffects: CreateAppEffects = (effectsCreator) =>
  effectsCreator
