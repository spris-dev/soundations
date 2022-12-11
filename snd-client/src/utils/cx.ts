type Cx = (...classes: (string | boolean | null | undefined)[]) => string
export const cx: Cx = (...classes) => {
  return classes.filter(isNotEmptyString).join(" ").trim()
}

type IsNotEmptyString = (val: Parameters<Cx>[number]) => boolean
const isNotEmptyString: IsNotEmptyString = (val) =>
  typeof val === "string" && val.length > 0
