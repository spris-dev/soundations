import { useEffect } from "preact/hooks"

import {
  createAppContext,
  PreactAppContext,
  useAppContext,
} from "snd-client/app-context"
import { Layout } from "snd-client/components/layout"
import { TrackSearch } from "snd-client/components/track-search"
import { TrackRecommendations } from "snd-client/components/track-recommendations"
import { TrackPlayer } from "snd-client/components/track-player"
import { UserPanel } from "snd-client/components/user-panel"
import { DialogRoot } from "snd-client/components/dialog-root"

const ctx = createAppContext()

export function AppInternal() {
  const { effects } = useAppContext()

  useEffect(() => {
    return effects.user.subscribe()
  }, [])

  return (
    <>
      <Layout trackSearch={<TrackSearch />} userPanel={<UserPanel />}>
        <TrackRecommendations />
        <TrackPlayer />
      </Layout>
      <DialogRoot />
    </>
  )
}

export function App() {
  return (
    <PreactAppContext.Provider value={ctx}>
      <AppInternal />
    </PreactAppContext.Provider>
  )
}
