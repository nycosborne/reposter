import axios, {AxiosRequestConfig, AxiosResponse, AxiosError} from "axios";

const axiosClient = axios.create({
    baseURL: `${import.meta.env.VITE_API_BASE_URL}/api`,
    headers: {
        // 'Content-Type': 'multipart/form-data',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',

    }
});

// @ts-expect-error Request interceptor
axiosClient.interceptors.request.use((config: AxiosRequestConfig) => {
    const token = localStorage.getItem('ACCESS_TOKEN');
    if (token) {
        config.headers = {
            ...config.headers,
            Authorization: `Token ${token}`
        };
    }
    return config;
}, (error: AxiosError) => {
    return Promise.reject(error);
});

// Response interceptor
axiosClient.interceptors.response.use((response: AxiosResponse) => {
    return response;
}, (error: AxiosError) => {
    const {response} = error;
    if (response) {
        if (response.status === 401) {
            localStorage.removeItem('ACCESS_TOKEN');
        } else if (response.status === 404) {
            // Show not found
        }
    }
    return Promise.reject(error);
});

export default axiosClient;
