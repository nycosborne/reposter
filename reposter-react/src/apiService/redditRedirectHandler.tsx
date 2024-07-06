import React, {useEffect} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
// import getAndSetAccessToken from './requestAccessToken';
import useAppContext from "../context/UseAppContext.tsx";
// import axios from "axios";
import axiosClient from "../axios-client.tsx";


// interface AccessTokenResponse {
//     message: string;
// }


const redditRedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    // const REDDIT_CLIENT_ID = import.meta.env.VITE_REDDIT_CLIENT_ID;
    // const REDDIT_CLIENT_SECRET = import.meta.env.VITE_REDDIT_CLIENT_SECRET;
    // const REDDIT_REDIRECT_URI = import.meta.env.VITE_REDDIT_REDIRECT_URI;
    const {user, setUser} = useAppContext();

    // const [authorizationCode, setAuthorizationCode] = useState<string | null>('');
    // const {user, setUser} = useAppContext();

    const searchParams = new URLSearchParams(location.search);
    console.log('redditRedirectHandler.searchParams:', searchParams);
    let code: string = searchParams.get('code') || '';
    console.log('code:', code);

    // const redditAccessToke = 'https://www.reddit.com/api/v1/access_token';
    // redditAccessToke.search = new URLSearchParams({
    //         grant_type: 'authorization_code',
    //         authorization_code: code,
    //         redirect_uri: REDDIT_REDIRECT_URI
    //     }
    // ).toString();
    // const redditRequestTokeString = redditAccessToke.toString();

    useEffect(() => {

        const payload: { code: string, account_type: string } = {
            code: code,
            account_type: 'reddit'
        };
        axiosClient.post('/services/passcode/', payload)
            .then((response) => {
                // todo - set the access token in the local storage OR NOT

                console.log('response from passcode', response.data);
                if (user) {
                    const updatedUser = {...user, reddit: true};
                    setUser(updatedUser);
                }
                navigate('/dashboard');
            })
            .catch((error) => {
                console.log('error', error);
            });

        // if (code !== null) {
        //     getToken().then((data) => {
        //         console.log('Access Token data:', data);
        //         // Redirect to the dashboard after successfully getting the access token
        //         if (user) {
        //             const updatedUser = {...user, reddit: true};
        //             setUser(updatedUser);
        //         }
        //         navigate('/dashboard');
        //     }).catch((error) => {
        //         console.error('Error:', error);
        //     });
        // } else {
        //     console.error('Authorization code not found');
        // }
    });


    // const getToken = async () => {
    //     const body = new URLSearchParams({
    //         grant_type: 'authorization_code',
    //         code: code, // Assuming 'code' is defined and holds the authorization code
    //         redirect_uri: REDDIT_REDIRECT_URI
    //     }).toString();
    //
    //     const data = await axios.post(
    //         redditAccessToke, // Ensure this variable holds the correct URL
    //         body,
    //         {
    //             headers: {
    //                 Authorization: `Basic ${btoa(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`)}`,
    //                 "Content-Type": "application/x-www-form-urlencoded",
    //             },
    //         }
    //     );
    //     console.log('redditRedirect.data:', data);
    //     return data.data;
    // };


    return (
        <div>
            <h2>auth/callbacking</h2>
            <h2>Processing...</h2>
        </div>
    );
};

export default redditRedirectHandler;
