import React, {useEffect} from 'react';
import {useNavigate, useLocation} from 'react-router-dom';
import getAndSetAccessToken from './requestAccessToken';
import useAppContext from "../context/UseAppContext.tsx";

// TODO: Need to make this a router component
// All callback will redirect to this component then I'll route to the specific API handler
const RedirectHandler: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    // const [authorizationCode, setAuthorizationCode] = useState<string | null>('');
    const {user, setUser} = useAppContext();
    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');

        if (code !== null) {
            getAndSetAccessToken(code, 'linkedin').then((data) => {
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
    });

    return (
        <div>
            <h2>auth/callbacking</h2>
            <h2>Processing...</h2>
        </div>
    );
};

export default RedirectHandler;
