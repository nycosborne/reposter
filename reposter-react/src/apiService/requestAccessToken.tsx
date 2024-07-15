import axiosClient from "../axios-client.tsx";
import useAppContext from "../context/UseAppContext.tsx";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";

interface AccessTokenResponse {
    message: string;
}

const getAndSetAccessToken = async (code: string, account_type: string): Promise<AccessTokenResponse> => {
    const payload: { code: string, account_type: string } = {
        code: code,
        account_type: account_type
    };

    const {user, setUser} = useAppContext();
    const navigate = useNavigate();

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');
        const state = searchParams.get('state');
        const message: string = '';
        axiosClient.post('/services/passcode/', payload)
            .then(() => {
                // todo - set the access token in the local storage OR NOT
                navigate('/dashboard', {replace: true});
                window.location.reload();
            })
            .catch((error) => {
                console.log('error', error);
            });
        // return {message: message};
        // TODO this should be better
        // Maybe I should uses a randomly generated string
        // one off string for each code request
    }, [user]);
    // const message: string = '';
    // axiosClient.post('/services/passcode/', payload)
    //     .then((response) => {
    //         // todo - set the access token in the local storage OR NOT
    //         return response.data;
    //     })
    //     .catch((error) => {
    //         console.log('error', error);
    //     });
    // return {message: message};


};

export default getAndSetAccessToken;
