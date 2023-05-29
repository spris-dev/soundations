import { FunctionalComponent } from "preact"

import { useAppContext } from "snd-client/app-context"
import { LoginDialog, SignupDialog } from "snd-client/components/dialogs"
import { OpStatus } from "snd-client/utils"

export const UserPanel: FunctionalComponent = () => {
  const {
    state: {
      user: { authState },
    },
    effects,
  } = useAppContext()

  if (authState.value.status === OpStatus.OK) {
    return (
      <div>
        {authState.value.result.name} (
        <button onClick={effects.user.logOut}>Log Out</button>)
      </div>
    )
  }

  return (
    <div>
      <button onClick={() => effects.dialog.open(<LoginDialog />)}>
        Log In
      </button>
      &nbsp;/&nbsp;
      <button onClick={() => effects.dialog.open(<SignupDialog />)}>
        Sign Up
      </button>
    </div>
  )
}
