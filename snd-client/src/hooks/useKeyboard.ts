import { useEffect } from "preact/hooks"

type KeypressHandler = (event: KeyboardEvent) => void

export type UseKeyboard = (params: { onKeyPress: KeypressHandler }) => void

const handlers: Set<KeypressHandler> = new Set()

const keypressListener: KeypressHandler = (event) => {
  for (const handler of handlers) {
    handler(event)
  }
}

export const useKeyboard: UseKeyboard = ({ onKeyPress }) => {
  useEffect(() => {
    if (handlers.size === 0) {
      addEventListener("keydown", keypressListener)
    }

    handlers.add(onKeyPress)

    return () => {
      handlers.delete(onKeyPress)

      if (handlers.size === 0) {
        removeEventListener("keydown", keypressListener)
      }
    }
  }, [onKeyPress])
}
