import { createAppContext, PreactAppContext } from "snd-client/app-context"
import { Layout } from "snd-client/components/layout"
import { TrackSearch } from "snd-client/components/track-search"
import { TrackRecommendations } from "snd-client/components/track-recommendations"
import { TrackPlayer } from "snd-client/components/track-player"

const ctx = createAppContext()

export function App() {
  return (
    <PreactAppContext.Provider value={ctx}>
      <Layout trackSearch={<TrackSearch />}>
        <TrackRecommendations />
        <TrackPlayer />
      </Layout>
    </PreactAppContext.Provider>
  )
}
