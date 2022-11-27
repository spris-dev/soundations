import { SoundationsApiClient } from "snd-server-api-client"

type CreateSoundationsApi = () => SoundationsApiClient

export const createSoundationsApi: CreateSoundationsApi = () => {
  return new SoundationsApiClient({
    BASE: "",
  })
}
