/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class HealthService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Health
     * @returns any Successful Response
     * @throws ApiError
     */
    public health(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/health',
        });
    }

}
