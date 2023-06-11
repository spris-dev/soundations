/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TracksRecommendationsResponse } from '../models/TracksRecommendationsResponse';
import type { TracksSearchResponse } from '../models/TracksSearchResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class TracksService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Tracks
     * @returns TracksSearchResponse Successful Response
     * @throws ApiError
     */
    public getTracks({
        q,
        limit = 5,
        offset,
    }: {
        q: string,
        limit?: number,
        offset?: number,
    }): CancelablePromise<TracksSearchResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/tracks',
            query: {
                'q': q,
                'limit': limit,
                'offset': offset,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Track Recommendations
     * @returns TracksRecommendationsResponse Successful Response
     * @throws ApiError
     */
    public getTrackRecommendations({
        trackId,
        limit = 6,
        offset,
    }: {
        trackId: string,
        limit?: number,
        offset?: number,
    }): CancelablePromise<TracksRecommendationsResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/tracks/{track_id}/recommendations',
            path: {
                'track_id': trackId,
            },
            query: {
                'limit': limit,
                'offset': offset,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Personal Recommendations
     * @returns TracksRecommendationsResponse Successful Response
     * @throws ApiError
     */
    public getPersonalRecommendations({
        prompt,
        limit = 6,
        offset,
    }: {
        prompt: string,
        limit?: number,
        offset?: number,
    }): CancelablePromise<TracksRecommendationsResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/tracks/personal_recommendations',
            query: {
                'prompt': prompt,
                'limit': limit,
                'offset': offset,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
