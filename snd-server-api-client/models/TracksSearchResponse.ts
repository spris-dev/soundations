/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SpotifyApiTrack } from './SpotifyApiTrack';

export type TracksSearchResponse = {
    items: Array<SpotifyApiTrack>;
    limit: number;
    offset: number;
    total: number;
};

