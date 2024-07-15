import axiosClient from "../axios-client.tsx";
import useAppContext from "../context/UseAppContext.tsx";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";

interface AccessTokenResponse {
    message: string;
}

const GetAndSetAccessToken = async (code: string, account_type: string): Promise<AccessTokenResponse> => {


    const {user} = useAppContext();
    const navigate = useNavigate();

    useEffect(() => {
        const payload: { code: string, account_type: string } = {
            code: code,
            account_type: account_type
        };
        axiosClient.post('/services/passcode/', payload)
            .then(() => {
                // todo - set the access token in the local storage OR NOT
                navigate('/dashboard', {replace: true});
                window.location.reload();
            })
            .catch((error) => {
                console.log('error', error);
            });
    }, [user, navigate, code, account_type]);

    return {message: 'Passed Code!'};


};

export default GetAndSetAccessToken;
