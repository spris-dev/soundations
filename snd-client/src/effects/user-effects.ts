import { effect } from "@preact/signals"

import { createAppEffects } from "snd-client/effects/create-effects"
import { OpStatus, decodeJwt } from "snd-client/utils"
import type { TokenRequestPayload } from "snd-server-api-client"

export const createUserEffects = createAppEffects((ctx, { cancelAll }) => {
  const {
    state: {
      user: { authState },
      dialog,
    },
    services: { soundationsApi, authStateStorage },
  } = ctx

  const logOut = () => {
    authState.value = { status: OpStatus.IDLE }
  }

  const logIn = (payload: TokenRequestPayload) => {
    authState.value = {
      status: OpStatus.LOADING,
      action: "login",
      payload,
    }
  }

  const signUp = (payload: TokenRequestPayload) => {
    authState.value = {
      status: OpStatus.LOADING,
      action: "signup",
      payload,
    }
  }

  const subscribe = () => {
    return cancelAll([
      effect(() => {
        // When dialog is closed but auth state is either loading or error
        // we reset it to "clean" idle state
        if (
          dialog.content.value === null &&
          authState.peek().status !== OpStatus.OK
        ) {
          authState.value = { status: OpStatus.IDLE }
        }
      }),

      effect(() => {
        if (authState.value.status === OpStatus.OK) {
          authStateStorage.set(authState.value.result)
        } else {
          authStateStorage.clear()
        }
      }),

      effect(async () => {
        if (authState.value.status !== OpStatus.LOADING) {
          return
        }

        try {
          const authApi =
            authState.value.action === "login"
              ? soundationsApi.users.login
              : soundationsApi.users.signup

          const { access_token } = await authApi.call(soundationsApi.users, {
            requestBody: authState.value.payload,
          })

          const { sub } = decodeJwt<{ sub: string }>(access_token)

          if (!sub) {
            throw new Error("Unexpected token format")
          }

          authState.value = {
            status: OpStatus.OK,
            result: {
              name: sub,
              token: access_token,
            },
          }

          ctx.effects.dialog.close()
        } catch (error) {
          console.error(error)
          authState.value = { status: OpStatus.ERROR, error }
        }
      }),
    ])
  }

  return {
    subscribe,
    logOut,
    logIn,
    signUp,
  }
})
