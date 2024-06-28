import axiosClient from "../axios-client.tsx";

interface AccessTokenResponse {
    message: string;
}

const getAndSetAccessToken = async (code: string): Promise<AccessTokenResponse> => {
    const payload: { code: string } = {
        code: code
    };

    let message :string = '';
    axiosClient.post('/services/passcode/', payload)
        .then((response) => {

        return response.data;
        })
        .catch((error) => {
            console.log('error', error);
        });
    return { message: message };
};

export default getAndSetAccessToken;
