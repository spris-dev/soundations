import { FunctionComponent } from "preact"

export type ButtonProps = {
  variant?: "primary" | "secondary" | "inline"
  onClick: (event: Event) => void
}

const variantToClassNameMap: Record<
  NonNullable<ButtonProps["variant"]>,
  string
> = {
  primary: "bg-color-active rounded-md border-2 border-color-primary",
  secondary:
    "bg-color-secondary-lessish rounded-md border-2 border-color-primary",
  inline: "",
}

export const Button: FunctionComponent<ButtonProps> = ({
  children,
  variant = "primary",
  onClick,
}) => {
  return (
    <button
      className={`h-full p-2 focus:outline focus:outline-2 ${variantToClassNameMap[variant]}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
