type Match = <T>(cb: (utils: MatchUtils) => T) => T
export const match: Match = (cb) => {
  return cb(matchUtils)
}

type MatchUtils = {
  assertNever: (_: never) => never
}
const matchUtils: MatchUtils = {
  assertNever: () => {
    throw new Error("Failed exhaustiveness check")
  },
}
