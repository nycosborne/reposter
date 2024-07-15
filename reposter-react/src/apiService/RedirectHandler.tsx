import React from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import GetAndSetAccessToken from './requestAccessToken';
import useAppContext from "../context/UseAppContext.tsx";

const LINKEDIN_STATE = import.meta.env.VITE_STATE;

const RedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const {user, setUser} = useAppContext();


    async function handleAccessToken(code: string, platform: string) {
        try {
            const data = await GetAndSetAccessToken(code, platform);
            console.log('Access Token:', data);
            // Redirect to the dashboard after successfully getting the access token
            if (user) {
                const updatedUser = {...user, linkedin: true};
                setUser(updatedUser);
            }
            navigate('/dashboard');
        } catch (error) {
            console.error('Error:', error);
        } finally {
            // setLoading(false);
        }
    }

    const searchParams = new URLSearchParams(location.search);
    const code = searchParams.get('code');
    const state = searchParams.get('state');

    // TODO this should be better
    // Maybe I should uses a randomly generated string
    // one off string for each code request
    // TODO: set up logging
    if (state !== LINKEDIN_STATE) {
        console.error('Invalid state:', state);
        return;
    }

    if (code !== null) {
        handleAccessToken(code, 'linkedin').then(r => {
            console.log('Access token:', r);
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

export default RedirectHandler;
