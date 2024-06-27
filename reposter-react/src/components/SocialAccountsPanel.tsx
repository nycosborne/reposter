import React from 'react';
import {Card, ListGroup, Container, Row} from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faLinkSlash} from "@fortawesome/free-solid-svg-icons";
import {IconProp} from '@fortawesome/fontawesome-svg-core';
import {useNavigate, useLocation} from "react-router-dom";
import axiosClient from "../axios-clinet.tsx";

const SocialAccountsCard = (): React.JSX.Element => {
    const {user} = useAppContext();
    const navigate = useNavigate();
    const location = useLocation();

    if (!user) {
        return <div>Loading...</div>
    }

    const handleRedditLink = () => {
        if(location.pathname != "/account")
            navigate("/account");

         // console.log('location.pathname', location.pathname)
    }

    const linkedinLink = () => {
        axiosClient.get('/services/request_code/')
            .then((response) => {
                // setUser(response.data);
                console.log('response', response);
            })
            .catch((error) => {
                console.log('error', error);
            });
    }

    const renderSocialAccount = (
        isLinked: boolean,
        icon: IconProp,
        color: string,
        accountStatusText: string,
        handleLink: () => void
    ) => (
        <ListGroup.Item action onClick={handleLink}>
            <Row>
                <FontAwesomeIcon icon={icon} size="2x" color={isLinked ? color : "gray"}/>
                {!isLinked && (
                    <div className="link-icon-container">
                        <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black" onClick={linkedinLink}/>
                        <a href={'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78rjltjnrm86ny&redirect_uri=https%3A%2F%2F45wvito15a.execute-api.us-east-1.amazonaws.com%2F&state=foobar&scope=openid%20profile%20w_member_social%20email'}>Link Account</a>
                    </div>
                )}
                <p>{accountStatusText} is: {isLinked ? "Linked" : "Unlinked"}</p>
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
                            "Reddit", handleRedditLink)}
                        {renderSocialAccount(user.linkedin, faLinkedin, "#0072b1",
                            "LinkedIn", handleRedditLink)}
                    </ListGroup>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsCard;
