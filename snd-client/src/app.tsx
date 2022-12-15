import { createAppContext, PreactAppContext } from "snd-client/app-context"
import { Layout } from "snd-client/components/layout"
import { TrackSearch } from "snd-client/components/track-search"
import { TrackRecommendations } from "snd-client/components/track-recommendations"

const ctx = createAppContext()

export function App() {
  return (
    <PreactAppContext.Provider value={ctx}>
      <Layout>
        <div className="w-full h-20 z-10 mb-8">
          <TrackSearch />
        </div>
        <TrackRecommendations />
      </Layout>
    </PreactAppContext.Provider>
  )
}
