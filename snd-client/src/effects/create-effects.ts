import type { AppContext } from "snd-client/app-context"

type AppEffectsResult<T> = T & {
  subscribe: () => () => void
}

type CancelAll = (cancellations: (() => void)[]) => () => void

const cancelAll: CancelAll = (cancellations) => {
  return () => cancellations.forEach((c) => c())
}

type CreateAppEffects = <T>(
  effectsCreator: (
    ctx: AppContext,
    utils: { cancelAll: CancelAll }
  ) => AppEffectsResult<T>
) => (ctx: AppContext) => AppEffectsResult<T>

export const createAppEffects: CreateAppEffects = (effectsCreator) => (ctx) => {
  return effectsCreator(ctx, { cancelAll })
}
