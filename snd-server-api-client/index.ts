/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export { SoundationsApiClient } from './SoundationsApiClient';

export { ApiError } from './core/ApiError';
export { BaseHttpRequest } from './core/BaseHttpRequest';
export { CancelablePromise, CancelError } from './core/CancelablePromise';
export { OpenAPI } from './core/OpenAPI';
export type { OpenAPIConfig } from './core/OpenAPI';

export type { HTTPValidationError } from './models/HTTPValidationError';
export type { SpotifyApiAlbum } from './models/SpotifyApiAlbum';
export type { SpotifyApiArtist } from './models/SpotifyApiArtist';
export type { SpotifyApiImage } from './models/SpotifyApiImage';
export type { SpotifyApiTrack } from './models/SpotifyApiTrack';
export type { TrackRecommendationsItem } from './models/TrackRecommendationsItem';
export type { TracksRecommendationsResponse } from './models/TracksRecommendationsResponse';
export type { TracksSearchResponse } from './models/TracksSearchResponse';
export type { ValidationError } from './models/ValidationError';

export { HealthService } from './services/HealthService';
export { TracksService } from './services/TracksService';
