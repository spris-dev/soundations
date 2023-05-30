import { FunctionalComponent } from "preact"
import { useEffect, useCallback } from "preact/hooks"

import { useAppContext } from "snd-client/app-context"
import { useKeyboard } from "snd-client/hooks"

export const DialogRoot: FunctionalComponent = () => {
  const {
    state: { dialog },
    effects,
  } = useAppContext()

  useEffect(() => {
    return effects.dialog.subscribe()
  }, [])

  const handleClickOutside = useCallback((event: Event) => {
    if (event.target === event.currentTarget) {
      effects.dialog.close()
    }
  }, [])

  const handleKeyPress = useCallback(
    (event: KeyboardEvent) => {
      if (dialog.content.value && event.code === "Escape") {
        effects.dialog.close()
      }
    },
    [dialog.content.value]
  )

  useKeyboard({ onKeyPress: handleKeyPress })

  if (!dialog.content.value) {
    return null
  }

  return (
    <div
      onClick={handleClickOutside}
      className="fixed top-0 left-0 w-full h-full z-100 flex items-center justify-center bg-color-secondary-lessish/75"
    >
      {dialog.content.value}
    </div>
  )
}
