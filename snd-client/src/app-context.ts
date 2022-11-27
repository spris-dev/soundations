import { createAppState } from "snd-client/app-state"
import { createAppEffects } from "snd-client/app-effects"
import { createAppServices } from "snd-client/app-services"

export type AppContext = {
  state: ReturnType<typeof createAppState>
  effects: ReturnType<typeof createAppEffects>
  services: ReturnType<typeof createAppServices>
}

type CreateAppContext = () => AppContext
export const createAppContext: CreateAppContext = () => {
  const ctx: AppContext = Object.create(null)

  const services = (ctx.services = createAppServices(ctx))
  const state = (ctx.state = createAppState())
  const effects = (ctx.effects = createAppEffects(ctx))

  return {
    state,
    effects,
    services,
  }
}
