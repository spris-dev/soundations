import { FunctionalComponent } from "preact"
import { useEffect, useState, useRef } from "preact/hooks"

import { useAppContext } from "snd-client/app-context"
import { Button } from "snd-client/components/button"
import { Input } from "snd-client/components/input"
import { Dialog } from "snd-client/components/dialogs"

export const LoginDialog: FunctionalComponent = () => {
  const {
    state: {
      user: { authState },
    },
    effects,
  } = useAppContext()

  useEffect(() => {
    return effects.user.subscribe()
  }, [])

  const formRef = useRef<HTMLFormElement>(null)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  return (
    <Dialog>
      <Dialog.Header>Log in</Dialog.Header>
      <Dialog.Body>
        <div className="flex flex-col w-full">
          <form ref={formRef}>
            <div>Username</div>
            <Input
              name="soundations-username"
              value={username}
              onChange={setUsername}
              type="text"
              minLength={4}
              maxLength={64}
              required
            />
            <div className="pt-4">Password</div>
            <Input
              name="soundations-password"
              value={password}
              onChange={setPassword}
              type="password"
              maxLength={64}
              required
            />
          </form>
        </div>
      </Dialog.Body>
      {authState.value.status === "ERROR" && (
        <Dialog.Error>{JSON.stringify(authState.value.error)}</Dialog.Error>
      )}
      <Dialog.Footer>
        <Dialog.FooterAction>
          <Button
            onClick={async () => {
              if (!formRef.current?.reportValidity()) {
                return
              }

              await effects.user.logIn({ username, password })
              effects.dialog.close()
            }}
          >
            Submit
          </Button>
        </Dialog.FooterAction>
        <Dialog.FooterAction>
          <Dialog.CancelButton />
        </Dialog.FooterAction>
      </Dialog.Footer>
    </Dialog>
  )
}
