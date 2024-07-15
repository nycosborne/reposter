import React, {useEffect} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import getAndSetAccessToken from './requestAccessToken';
import useAppContext from "../context/UseAppContext.tsx";

const LINKEDIN_STATE = import.meta.env.VITE_STATE;
// TODO: Need to make this a router component
// All callback will redirect to this component then I'll route to the specific API handler

const RedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    // const [authorizationCode, setAuthorizationCode] = useState<string | null>('');
    const {user, setUser} = useAppContext();

    // const [loading, setLoading] = useState(false);

    async function handleAccessToken(code: string, platform: string) {
        try {
            const data = await getAndSetAccessToken(code, platform);
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

    // useEffect(() => {
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
    // if (loading) {
    //     return;
    // }
    // setLoading(true);
    if (code !== null) {
        handleAccessToken(code, 'linkedin').then(r => {
            console.log('Access token:', r);
        });
    } else {
        console.error('Authorization code not found');
    }
    // });


    return (
        <div>
            <h2>auth/callbacking</h2>
            <h2>Processing...</h2>
        </div>
    );
};

export default RedirectHandler;
