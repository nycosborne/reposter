import React, {useEffect, useState} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import getAndSetAccessToken from "./requestAccessToken.tsx";


const RedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [authorizationCode, setAuthorizationCode] = useState<string | null>('');

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');

        if (authorizationCode != null && code !== null) {
            setAuthorizationCode(code);
            // Handle the authorization code (e.g., send it to your backend for further processing)
            console.log('Authorization Code:', code);
            console.log('Authorization CodeState:', authorizationCode);
            // Optionally, navigate to a different page or perform some other action
            // navigate('/some-other-page');
            getAndSetAccessToken(code)
                .then((data) => {
                    console.log('Access Token:', data.access_token);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        } else {
            console.error('Authorization code not found');
        }
    }, [location, navigate]);

    return (
        <div>
            <h2>auth/callbacking</h2>
            {authorizationCode ? <h2>CODE!!!: {authorizationCode}</h2> : <h2>Processing...</h2>}
        </div>
    );
};

export default RedirectHandler;