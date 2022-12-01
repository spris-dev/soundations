/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SpotifyApiAlbum } from './SpotifyApiAlbum';
import type { SpotifyApiArtist } from './SpotifyApiArtist';

export type SoundationsTrack = {
    id: string;
    name: string;
    album: SpotifyApiAlbum;
    artists: Array<SpotifyApiArtist>;
    duration_ms: number;
    href: string;
    preview_url: string;
};

