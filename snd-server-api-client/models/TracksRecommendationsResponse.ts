/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TrackRecommendationsItem } from './TrackRecommendationsItem';

export type TracksRecommendationsResponse = {
    items: Array<TrackRecommendationsItem>;
    limit: number;
    offset: number;
    total: number;
};

