import React from 'react';
import {Card, ListGroup, Container, Row, Col} from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faLinkSlash} from "@fortawesome/free-solid-svg-icons";
import {IconProp} from '@fortawesome/fontawesome-svg-core';
import {useNavigate, useLocation} from "react-router-dom";
// import axiosClient from "../axios-client.tsx";


// Define the parameters for the LinkedIn OAuth 2.0 request
const clientId = import.meta.env.VITE_CLIENT_ID;
const redirectUri = import.meta.env.VITE_REDIRECT_URI;
const state = import.meta.env.VITE_STATE;
const scope = import.meta.env.VITE_SCOPE;

// Construct the LinkedIn OAuth 2.0 authorization URL
const linkedinAuthUrl = new URL('https://www.linkedin.com/oauth/v2/authorization');
const redditAuthUrl = new URL('https://www.nycosborne.com/oauth2/authorize/');

linkedinAuthUrl.search = new URLSearchParams({
        response_type: 'code',
        client_id: clientId,
        redirect_uri: redirectUri,
        state: state,
        scope: scope
    }
).toString();

redditAuthUrl.search = new URLSearchParams({
        response_type: 'code',
        client_id: clientId,
        redirect_uri: redirectUri,
        state: state,
        scope: scope
    }
).toString();

const linkedinAuthUrlString = linkedinAuthUrl.toString();
const redditAuthUrlString = redditAuthUrl.toString();


interface SocialAccountsCardProps {
    showLink: boolean;
}

const SocialAccountsPanel = ({showLink}: SocialAccountsCardProps): React.JSX.Element => {

    const {user} = useAppContext();
    const navigate = useNavigate();
    const location = useLocation();

    if (!user) {
        return <div>Loading...</div>
    }

    const navigateToAccount = () => {
        if (location.pathname != "/account")
            navigate("/account");
    }

    const renderSocialAccount = (
        isLinked: boolean,
        icon: IconProp,
        color: string,
        accountStatusText: string,
        handleLink: () => void,
        userAuthLink: string
    ) => (
        <ListGroup.Item action onClick={handleLink}>
            <Row>
                <Col>
                    <FontAwesomeIcon icon={icon} size="2x" color={isLinked ? color : "gray"}/>
                    {!isLinked && (
                        <div className="link-icon-container">
                            <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
                        </div>)}
                </Col>
                <Col>
                    <h5>{accountStatusText}</h5>
                    <p>Account is: {isLinked ? "Linked" : "Unlinked"}</p>
                    {showLink && !isLinked && (
                        <a href={userAuthLink}>Link Account</a>
                    )}
                    {/*todo: here for development*/}
                    {showLink && (
                        <a href={userAuthLink}>Link Account</a>
                    )}
                </Col>
            </Row>
        </ListGroup.Item>
    );

    return (
        <Container>
            <Card>
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Social Accounts Status
                    </Card.Title>
                    <ListGroup>
                        {renderSocialAccount(user.reddit, faRedditAlien, "#FF5700",
                            "Reddit", navigateToAccount, redditAuthUrlString)}
                        {renderSocialAccount(user.linkedin, faLinkedin, "#0072b1",
                            "LinkedIn", navigateToAccount, linkedinAuthUrlString)}
                    </ListGroup>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsPanel;
