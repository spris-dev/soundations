import { VNode } from "preact"
import { noop } from "lodash-es"

import { createAppEffects } from "snd-client/effects/create-effects"

export const createDialogEffects = createAppEffects((ctx) => {
  const {
    state: {
      dialog: { content },
    },
  } = ctx

  const open = (value: VNode) => {
    content.value = value
  }

  const close = () => {
    content.value = null
  }

  const subscribe = () => noop

  return {
    subscribe,
    open,
    close,
  }
})
