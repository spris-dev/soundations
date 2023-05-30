import { FunctionalComponent } from "preact"

import { useAppContext } from "snd-client/app-context"
import { Button } from "snd-client/components/button"

type DialogType = FunctionalComponent & {
  Header: typeof DialogHeader
  Body: typeof DialogBody
  Footer: typeof DialogFooter
  FooterAction: typeof DialogFooterAction
  CancelButton: typeof DialogCancelButton
  Error: typeof DialogError
}

export const DialogContainer: FunctionalComponent = ({ children }) => {
  return (
    <div className="w-screen h-screen md:w-3/5 md:max-w-3xl md:h-3/5 flex flex-col bg-color-background rounded-md border-2 border-color-primary">
      {children}
    </div>
  )
}

export const DialogHeader: FunctionalComponent = ({ children }) => {
  return (
    <div className="w-full h-16 p-4 flex shrink-0 items-center text-xl">
      {children}
    </div>
  )
}

export const DialogBody: FunctionalComponent = ({ children }) => {
  return <div className="w-full p-4 grow flex items-center">{children}</div>
}

export const DialogFooter: FunctionalComponent = ({ children }) => {
  return (
    <div className="w-full h-20 p-4 flex shrink-0 items-center">{children}</div>
  )
}

export const DialogFooterAction: FunctionalComponent = ({ children }) => {
  return <div className="h-full pr-4">{children}</div>
}

export const DialogCancelButton: FunctionalComponent = () => {
  const { effects } = useAppContext()

  return (
    <Button onClick={effects.dialog.close} variant="secondary">
      Cancel
    </Button>
  )
}

export const DialogError: FunctionalComponent = ({ children }) => {
  return (
    <div className="w-full h-20 p-4 shrink-0 items-center text-red-500 rounded-md border-2 border-red-500 overflow-auto">
      {children}
    </div>
  )
}

export const Dialog: DialogType = Object.assign(DialogContainer, {
  Header: DialogHeader,
  Body: DialogBody,
  Footer: DialogFooter,
  FooterAction: DialogFooterAction,
  CancelButton: DialogCancelButton,
  Error: DialogError,
})
