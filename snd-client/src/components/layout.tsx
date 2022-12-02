import { FunctionalComponent } from "preact"

type LayoutProps = Record<never, never>

export const Layout: FunctionalComponent<LayoutProps> = ({ children }) => {
  return (
    <div className="w-full h-full p-8 text-color-primary">
      <div className="uppercase mb-2">Soundations</div>
      <div className="h-full max-w-lg">{children}</div>
    </div>
  )
}
