import React, {useEffect} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import useAppContext from "../context/UseAppContext.tsx";
import getAndSetAccessToken from "./requestAccessToken.tsx";
//
//
// interface AccessTokenResponse {
//     message: string;
// }
const REDDIT_STATE = import.meta.env.VITE_REDDIT_STATE;

const RedditRedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const {user, setUser} = useAppContext();

    // const [authorizationCode, setAuthorizationCode] = useState<string | null>('');
    // const {user, setUser} = useAppContext();

    const searchParams = new URLSearchParams(location.search);
    console.log('redditRedirectHandler.searchParams:', searchParams);
    const code: string = searchParams.get('code') || '';
    const state: string = searchParams.get('state') || '';
    console.log('code:', code);

    useEffect(() => {
        // TODO this should be better
        // Maybe I should uses a randomly generated string
        // one off string for each code request
        // TODO: set up logging
        if (state !== REDDIT_STATE) {
            console.error('Invalid state:', state);
            return
        }
        if (code !== null) {
            getAndSetAccessToken(code, 'reddit').then((data) => {
                console.log('Access Token:', data);
                // Redirect to the dashboard after successfully getting the access token
                if (user) {
                    const updatedUser = {...user, linkedin: true};
                    setUser(updatedUser);
                }
                navigate('/dashboard');
            }).catch((error) => {
                console.error('Error:', error);
            });
        } else {
            console.error('Authorization code not found');
        }
        // axiosClient.post('/services/passcode/', payload)
        //     .then((response) => {
        //         // todo - set the access token in the local storage OR NOT
        //
        //         console.log('response from passcode', response.data);
        //         if (user) {
        //             const updatedUser = {...user, reddit: true};
        //             setUser(updatedUser);
        //         }
        //         navigate('/dashboard');
        //     })
        //     .catch((error) => {
        //         console.log('error', error);
        //     });

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

    // redditAccessToke.search = new URLSearchParams({
    //         grant_type: 'authorization_code',
    //         authorization_code: code,
    //         redirect_uri: REDDIT_REDIRECT_URI
    //     }
    // ).toString();
    // const redditRequestTokeString = redditAccessToke.toString();

    // This function is used to get the access token from Reddit
    // const getToken = async () => {
    //     const redditAccessToke = 'https://www.reddit.com/api/v1/access_token';
    //     const body = new URLSearchParams({
    //         grant_type: 'authorization_code',
    //         code: code, // Assuming 'code' is defined and holds the authorization code
    //         redirect_uri: REDDIT_REDIRECT_URI
    //     }).toString();
    //
    //
    //     const data = await axios.post(
    //         redditAccessToke, // Ensure this variable holds the correct URL
    //         body,
    //         {
    //             headers: {
    //                 Authorization: `Basic ${btoa(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`)}`,
    //                 "Content-Type": "application/x-www-form-urlencoded",
    //                 'User-Agent': 'reposter/0.0.1 (by u/nycosborne)',
    //             },
    //         }
    //     );
    //     console.log('body:', body);
    //     console.log('headers', body);
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

export default RedditRedirectHandler;
