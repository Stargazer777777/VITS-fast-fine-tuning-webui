import axios, { AxiosError } from 'axios';
import type { AxiosRequestConfig } from 'axios';
import { ElMessage } from 'element-plus/es';
export const httpInstance = axios.create();

export type BkResponse = {
  data: any; // 出错时这一项将没有
  code?: number;
  msg?: string;
  success?: boolean;
};

export type BkException = {
  detail: string;
};

httpInstance.defaults.baseURL = import.meta.env.HTTP_BASEURL;

export interface HttpOption {
  noAlert?: true;
}

export const $http = async (
  config: AxiosRequestConfig,
  httpOption?: HttpOption
) => {
  try {
    const axiosResponse = await httpInstance<BkResponse>(config);
    const bkResponse = axiosResponse.data;

    return bkResponse;
  } catch (err) {
    if (err instanceof AxiosError) {
      let errMsg = 'unknown';
      if (err.response?.data) {
        const exception: BkException = err.response.data;
        errMsg = exception.detail;
      }
      console.log('here');

      if (!httpOption?.noAlert) {
        ElMessage.error(errMsg);
      }
    }
    throw err;
  }
};
