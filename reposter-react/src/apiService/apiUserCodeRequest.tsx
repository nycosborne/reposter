import React from 'react';

// Define the parameters for the LinkedIn OAuth 2.0 request
const clientId = '78rjltjnrm86ny';
const redirectUri = encodeURIComponent('https://45wvito15a.execute-api.us-east-1.amazonaws.com/');
const state = 'foobar';
const scope = encodeURIComponent('openid profile w_member_social email');

// Construct the LinkedIn OAuth 2.0 authorization URL
const linkedinAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&state=${state}&scope=${scope}`;

// Define a functional component that makes the GET request
const ApiUserCodeRequest: React.FC = () => {
    const handleLinkedInAuth = () => {
        window.location.href = linkedinAuthUrl;
    };

    return (
        <div>
            <button onClick={handleLinkedInAuth}>Authorize with LinkedIn</button>
        </div>
    );
};

export default ApiUserCodeRequest;
