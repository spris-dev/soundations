/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Token } from '../models/Token';
import type { TokenRequestForm } from '../models/TokenRequestForm';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class UsersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Login For Access Token
     * @returns Token Successful Response
     * @throws ApiError
     */
    public loginForAccessToken({
        requestBody,
    }: {
        requestBody: TokenRequestForm,
    }): CancelablePromise<Token> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Signup For Access Token
     * @returns Token Successful Response
     * @throws ApiError
     */
    public signupForAccessToken({
        requestBody,
    }: {
        requestBody: TokenRequestForm,
    }): CancelablePromise<Token> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
