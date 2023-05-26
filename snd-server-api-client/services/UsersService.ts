/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Token } from '../models/Token';

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
        username,
        password,
    }: {
        username: string,
        password: string,
    }): CancelablePromise<Token> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/login',
            query: {
                'username': username,
                'password': password,
            },
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
        username,
        password,
    }: {
        username: string,
        password: string,
    }): CancelablePromise<Token> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/signup',
            query: {
                'username': username,
                'password': password,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
