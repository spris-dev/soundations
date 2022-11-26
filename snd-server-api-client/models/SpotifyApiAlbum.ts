/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SpotifyApiImage } from './SpotifyApiImage';

export type SpotifyApiAlbum = {
    id: string;
    name: string;
    release_date: string;
    images: Array<SpotifyApiImage>;
};

