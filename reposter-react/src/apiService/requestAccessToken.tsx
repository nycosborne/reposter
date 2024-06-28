import axiosClient from "../axios-client.tsx";

interface AccessTokenResponse {
    message: string;
}

const getAndSetAccessToken = async (code: string): Promise<AccessTokenResponse> => {
    const payload: { code: string } = {
        code: code
    };

    const message :string = '';

    axiosClient.post('/services/passcode/', payload)
        .then((response) => {
            // todo - set the access token in the local storage OR NOT

        return response.data;
        })
        .catch((error) => {
            console.log('error', error);
        });
    return { message: message };
};

export default getAndSetAccessToken;
