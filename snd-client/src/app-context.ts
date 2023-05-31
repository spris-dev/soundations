import { createContext } from "preact"
import { useContext } from "preact/hooks"

import { createAppState } from "snd-client/app-state"
import { createAppEffects } from "snd-client/app-effects"
import { createAppServices } from "snd-client/app-services"

import { ToReadonlySignalDeep } from "snd-client/utils"

export type AppContext = {
  state: ReturnType<typeof createAppState>
  effects: ReturnType<typeof createAppEffects>
  services: ReturnType<typeof createAppServices>
}

type CreateAppContext = () => AppContext
export const createAppContext: CreateAppContext = () => {
  const ctx: AppContext = Object.create(null)

  const services = (ctx.services = createAppServices(ctx))
  const state = (ctx.state = createAppState(ctx))
  const effects = (ctx.effects = createAppEffects(ctx))

  return {
    state,
    effects,
    services,
  }
}

export const PreactAppContext = createContext<AppContext | null>(null)

type UseAppContext = () => Omit<AppContext, "state"> & {
  state: ToReadonlySignalDeep<AppContext["state"]>
}
export const useAppContext: UseAppContext = () => {
  const ctx = useContext(PreactAppContext)

  if (!ctx) {
    throw new Error(
      `AppContext not found, please make sure ${PreactAppContext} was used`
    )
  }

  return ctx
}
