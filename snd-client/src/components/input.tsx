import { Signal } from "@preact/signals"
import { FunctionalComponent, VNode, cloneElement, JSX } from "preact"
import { useCallback } from "preact/hooks"

type InputProps = Omit<
  JSX.HTMLAttributes<HTMLInputElement>,
  "value" | "onChange" | "icon" | "placeholder"
> & {
  icon?: VNode
  value?: string | Signal<string>
  placeholder?: string | Signal<string>
  onChange?: (value: string) => void
}

export const Input: FunctionalComponent<InputProps> = ({
  icon,
  value,
  onChange,
  placeholder,
  ...rest
}) => {
  const handleInput = useCallback(
    (event: Event) => {
      if (event.target instanceof HTMLInputElement) {
        onChange?.(event.target.value)
      }
    },
    [onChange]
  )

  return (
    <div className="flex relative w-full h-full font-bold text-lg shadow-md rounded-md border-2 border-color-primary focus-within:border-color-active bg-color-background">
      {icon && (
        <div className="shrink-0 grow h-full flex items-center ml-2 mr-2">
          {cloneElement(icon, {
            className: "h-1/2 stroke-color-secondary stroke-2",
          })}
        </div>
      )}
      <input
        {...rest}
        value={value}
        onInput={handleInput}
        placeholder={placeholder}
        type="text"
        className="shrink w-full h-full block placeholder:italic focus:outline-none rounded-md bg-color-background"
      />
    </div>
  )
}
