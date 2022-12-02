import { createAppContext, PreactAppContext } from "snd-client/app-context"
import { Layout } from "snd-client/components/layout"
import { TrackSearch } from "snd-client/components/track-search"

const ctx = createAppContext()

export function App() {
  return (
    <PreactAppContext.Provider value={ctx}>
      <Layout>
        <div className="w-full h-20">
          <TrackSearch />
        </div>
      </Layout>
    </PreactAppContext.Provider>
  )
}
