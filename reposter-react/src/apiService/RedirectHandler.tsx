import React, {useEffect} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';

const RedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    let authorizationCode: string | null = '';

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        authorizationCode = searchParams.get('code');

        if (authorizationCode) {
            // Handle the authorization code (e.g., send it to your backend for further processing)
            console.log('Authorization Code:', authorizationCode);

            // Optionally, navigate to a different page or perform some other action
            // navigate('/some-other-page');9
        } else {
            console.error('Authorization code not found');
        }
    }, [location, navigate]);

    return (
        <div>
            <h2>auth/callbacking</h2>
            {/*todo this need to be state*/}
            {authorizationCode ? <h2>CODE!!!: {authorizationCode}</h2> : <h2>Processing...</h2>}
        </div>
    );
};

export default RedirectHandler;