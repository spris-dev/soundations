import { FunctionalComponent } from "preact"

type LayoutProps = Record<never, never>

export const Layout: FunctionalComponent<LayoutProps> = ({ children }) => {
  return (
    <div className="w-full min-h-full overflow-x-hidden p-8 text-color-primary bg-color-background relative z-0 overflow-hidden">
      <div className="uppercase italic text-4xl mb-16">Soundations</div>
      <div className="h-full w-full flex justify-center">
        <div className="max-w-lg w-full">{children}</div>
      </div>
    </div>
  )
}
