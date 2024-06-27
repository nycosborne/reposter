import axiosClient from "../axios-client.tsx";

interface AccessTokenResponse {
    access_token: string;
    expires_in: number;
}

const getAccessToken = async (code: string): Promise<AccessTokenResponse> => {
    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    };

    const params = new URLSearchParams();
    params.append('grant_type', 'authorization_code');
    params.append('code', code);
    params.append('client_id', import.meta.env.VITE_CLIENT_ID || '');
    params.append('client_secret', import.meta.env.VITE_CLIENT_SECRET || '');
    params.append('redirect_uri', import.meta.env.VITE_REDIRECT_URI || '');

    try {
        const response = await axiosClient.post<AccessTokenResponse>(
            'https://www.linkedin.com/oauth/v2/accessToken',
            params,
            { headers, baseURL: '' }  // Override baseURL for this request
        );
        console.log('Access Token Response:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error requesting access token:', error);
        throw error;
    }
};

export default getAccessToken;
