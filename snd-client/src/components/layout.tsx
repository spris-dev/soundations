import { FunctionalComponent, VNode } from "preact"

type LayoutProps = {
  trackSearch: VNode
}

export const Layout: FunctionalComponent<LayoutProps> = ({
  children,
  trackSearch,
}) => {
  return (
    <div className="w-full min-h-full text-color-primary bg-color-background relative z-0 pt-32 pb-32">
      <div className="fixed top-0 left-0 w-full z-10">
        <div className="relative m-4 flex justify-center items-center">
          <div className="absolute left-0 italic inline-block text-4xl pt-1 pb-1 pl-2 pr-2 rounded-md bg-gradient-to-r to-color-active-lessish from-color-secondary-lessish">
            soundations
          </div>
          <div className="max-w-xl w-full h-20 shadow-xl shadow-color-background">
            {trackSearch}
          </div>
        </div>
      </div>

      <div className="h-full w-full flex justify-center">
        <div className="max-w-lg w-full">{children}</div>
      </div>
    </div>
  )
}
