export type DecodeJwt = <T>(value: string) => Partial<T>

export const decodeJwt: DecodeJwt = (value) => {
  const [, payload] = value.split(".")

  if (!payload) {
    return {}
  }

  try {
    return JSON.parse(atob(payload))
  } catch {
    return {}
  }
}
