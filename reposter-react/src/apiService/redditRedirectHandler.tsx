import React from 'react';
import {useLocation} from 'react-router-dom';
import useAppContext from "../context/UseAppContext.tsx";
import GetAndSetAccessToken from "./requestAccessToken.tsx";

const REDDIT_STATE = import.meta.env.VITE_REDDIT_STATE;

const RedditRedirectHandler: React.FC = () => {
    const location = useLocation();
    const {user, setUser} = useAppContext();


    const searchParams = new URLSearchParams(location.search);
    console.log('redditRedirectHandler.searchParams:', searchParams);
    const code: string = searchParams.get('code') || '';
    const state: string = searchParams.get('state') || '';
    console.log('code:', code);

    // useEffect(() => {
        // TODO this should be better
        // Maybe I should uses a randomly generated string
        // one off string for each code request
        // TODO: set up logging
        if (state !== REDDIT_STATE) {
            console.error('Invalid state:', state);
            return
        }
        if (code !== null) {
            GetAndSetAccessToken(code, 'reddit').then((data) => {
                console.log('Access Token:', data);
                // Redirect to the dashboard after successfully getting the access token
                if (user) {
                    const updatedUser = {...user, linkedin: true};
                    setUser(updatedUser);
                }
            }).catch((error) => {
                console.error('Error:', error);
            });
        } else {
            console.error('Authorization code not found');
        }

    return (
        <div>
            <h2>auth/callbacking</h2>
            <h2>Processing...</h2>
        </div>
    );
};

export default RedditRedirectHandler;
