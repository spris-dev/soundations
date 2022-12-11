import type { Signal, ReadonlySignal } from "@preact/signals"

type primitive = string | number | boolean | undefined | null

export type ToReadonlySignal<T> = T extends Signal<infer K>
  ? ReadonlySignal<K>
  : T extends primitive
  ? T
  : ToReadonlySignalDeep<T>

export type ToReadonlySignalDeep<T> = {
  readonly [P in keyof T]: ToReadonlySignal<T[P]>
}
