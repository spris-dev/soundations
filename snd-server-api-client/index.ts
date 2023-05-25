/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export { SoundationsApiClient } from './SoundationsApiClient';

export { ApiError } from './core/ApiError';
export { BaseHttpRequest } from './core/BaseHttpRequest';
export { CancelablePromise, CancelError } from './core/CancelablePromise';
export { OpenAPI } from './core/OpenAPI';
export type { OpenAPIConfig } from './core/OpenAPI';

export type { Body_login_for_access_token } from './models/Body_login_for_access_token';
export type { HTTPValidationError } from './models/HTTPValidationError';
export type { RecommendedTrack } from './models/RecommendedTrack';
export type { SoundationsTrack } from './models/SoundationsTrack';
export type { SpotifyApiAlbum } from './models/SpotifyApiAlbum';
export type { SpotifyApiArtist } from './models/SpotifyApiArtist';
export type { SpotifyApiImage } from './models/SpotifyApiImage';
export type { Token } from './models/Token';
export type { TrackRecommendationsItem } from './models/TrackRecommendationsItem';
export type { TracksRecommendationsResponse } from './models/TracksRecommendationsResponse';
export type { TracksSearchResponse } from './models/TracksSearchResponse';
export type { User } from './models/User';
export type { ValidationError } from './models/ValidationError';

export { DefaultService } from './services/DefaultService';
export { HealthService } from './services/HealthService';
export { TracksService } from './services/TracksService';
