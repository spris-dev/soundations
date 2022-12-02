import type { VNode } from "preact"

type Rndr = <T extends VNode | null>(cb: (utils: RndrUtils) => T) => T
export const rndr: Rndr = (cb) => {
  return cb(rndrUtils)
}

type RndrUtils = {
  assertNever: (_: never) => never
}
const rndrUtils: RndrUtils = {
  assertNever: () => {
    throw new Error("Failed exhaustiveness check")
  },
}
