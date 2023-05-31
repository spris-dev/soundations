import { isObject, isString } from "lodash-es"
import type { AppContext } from "snd-client/app-context"
import type { AuthStateResult } from "snd-client/app-state"

type Storage = {
  get: <T>(key: string, validate?: (v: T) => boolean) => T | null
  set: <T>(key: string, value: T) => void
  delete: (key: string) => void
}

type CreateStorage = (ctx: AppContext) => Storage

const KEY_PREFIX = "__snd_"

const getKey = (key: string) => `${KEY_PREFIX}${key}`

export const createStorage: CreateStorage = () => {
  return {
    get(key, validate) {
      try {
        const valueString = localStorage.getItem(getKey(key))

        if (valueString == null) {
          return null
        }

        const value = JSON.parse(valueString)

        if (validate && !validate(value)) {
          return null
        }

        return value
      } catch {
        return null
      }
    },

    set(key, value) {
      localStorage.setItem(getKey(key), JSON.stringify(value))
    },

    delete(key) {
      localStorage.removeItem(getKey(key))
    },
  }
}

type CreateEntityStorage = <T>(params: {
  key: string
  validate: (v: T) => boolean
}) => (ctx: AppContext) => {
  get: () => T | null
  set: (value: T) => void
  clear: () => void
}

const createEntityStorage: CreateEntityStorage =
  ({ key, validate }) =>
  (ctx) => {
    return {
      get() {
        return ctx.services.storage.get(key, validate)
      },

      set(value) {
        return ctx.services.storage.set(key, value)
      },

      clear() {
        return ctx.services.storage.delete(key)
      },
    }
  }

export const createAuthStateStorage = createEntityStorage<AuthStateResult>({
  key: "auth",
  validate: (value) => {
    return isObject(value) && isString(value.name) && isString(value.token)
  },
})
