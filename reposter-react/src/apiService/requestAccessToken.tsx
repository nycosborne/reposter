import axiosClient from "../axios-client.tsx";
import useAppContext from "../context/UseAppContext.tsx";
import {useEffect} from "react";

interface AccessTokenResponse {
    message: string;
}

const getAndSetAccessToken = async (code: string, account_type: string): Promise<AccessTokenResponse> => {

    const {user, setUser} = useAppContext();

    const payload: { code: string, account_type: string } = {
        code: code,
        account_type: account_type
    };

    useEffect(() => {
        axiosClient.post('/services/passcode/', payload)
            .then((response) => {
                // todo - set the access token in the local storage OR NOT
                setUser(response.data);
                return response.data;
            })
            .catch((error) => {
                console.log('error', error);
            });
    }, [user]);
    return {message: 'Updated user'};
    // const message: string = '';
    // axiosClient.post('/services/passcode/', payload)
    //     .then((response) => {
    //         // todo - set the access token in the local storage OR NOT
    //         setUser(response.data);
    //         return response.data;
    //     })
    //     .catch((error) => {
    //         console.log('error', error);
    //     });
    // return {message: message};
};

export default getAndSetAccessToken;
