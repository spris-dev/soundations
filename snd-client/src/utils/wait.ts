type Wait = (delay: number) => Promise<void>

export const wait: Wait = (delay) => {
  return new Promise((resolve) => {
    setTimeout(resolve, delay)
  })
}
