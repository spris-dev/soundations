/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SoundationsTrack } from './SoundationsTrack';

export type TracksSearchResponse = {
    items: Array<SoundationsTrack>;
    limit: number;
    offset: number;
    total: number;
};

