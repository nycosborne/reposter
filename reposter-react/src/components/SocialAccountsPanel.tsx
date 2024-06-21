import React from 'react';
import {Card, ListGroup, Container, Row} from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faLinkSlash} from "@fortawesome/free-solid-svg-icons";
import {IconProp} from '@fortawesome/fontawesome-svg-core';
import {useNavigate, useLocation} from "react-router-dom";

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

         console.log('location.pathname', location.pathname)
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
                        <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
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
