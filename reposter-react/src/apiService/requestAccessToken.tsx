import axiosClient from "../axios-client.tsx";

interface AccessTokenResponse {
    message: string;
}

const getAndSetAccessToken = async (code: string, account_type: string): Promise<AccessTokenResponse> => {
    const payload: { code: string, account_type: string } = {
        code: code,
        account_type: account_type
    };

    const message: string = '';
    axiosClient.post('/services/passcode/', payload)
        .then((response) => {
            // todo - set the access token in the local storage OR NOT
            return response.data;
        })
        .catch((error) => {
            console.log('error', error);
        });
    return {message: message};
};

export default getAndSetAccessToken;
