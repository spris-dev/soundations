import { SoundationsApiClient } from "snd-server-api-client"

import type { AppContext } from "snd-client/app-context"
import { OpStatus } from "snd-client/utils"

type CreateSoundationsApi = (ctx: AppContext) => SoundationsApiClient

export const createSoundationsApi: CreateSoundationsApi = (ctx) => {
  return new SoundationsApiClient({
    BASE: "",
    WITH_CREDENTIALS: true,
    TOKEN: () => {
      const authState = ctx.state.user.authState.peek()

      if (authState.status === OpStatus.OK) {
        return Promise.resolve(authState.result.token)
      }

      return Promise.resolve("")
    },
  })
}
