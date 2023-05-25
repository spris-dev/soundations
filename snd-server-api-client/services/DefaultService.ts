/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_for_access_token } from '../models/Body_login_for_access_token';
import type { Token } from '../models/Token';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class DefaultService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Login For Access Token
     * @returns Token Successful Response
     * @throws ApiError
     */
    public loginForAccessToken({
        formData,
    }: {
        formData: Body_login_for_access_token,
    }): CancelablePromise<Token> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Users Me
     * @returns User Successful Response
     * @throws ApiError
     */
    public readUsersMe({
        requestBody,
    }: {
        requestBody: User,
    }): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/me/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Own Items
     * @returns any Successful Response
     * @throws ApiError
     */
    public readOwnItems({
        requestBody,
    }: {
        requestBody: User,
    }): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/me/items/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
