import React from 'react';
import {Card, Container, Row, Col} from 'react-bootstrap';
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {useNavigate, useLocation} from "react-router-dom";
import {User} from "../types/types.tsx";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faLinkSlash} from "@fortawesome/free-solid-svg-icons";


interface SocialAccountsCardProps {
    user: User;
}

const SocialAccountsPostStatusBar = ({user}: SocialAccountsCardProps): React.JSX.Element => {


    const navigate = useNavigate();
    const location = useLocation();


    const selectService = () => {
        if (location.pathname != "/account")
            navigate("/account");
    }

    return (
        <Container>
            <Card className="dashboard-panel">
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Post Status
                    </Card.Title>
                    <Container>
                        <Row className="align-items-center">
                            <Col xs="auto">
                                <Row>
                                    <Col onClick={selectService}>
                                        <FontAwesomeIcon icon={faRedditAlien} size="2x"
                                                         color={user.reddit ? "#FF5700" : "gray"}/>
                                        {!user.reddit && (
                                            <div className="link-icon-container">
                                                <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
                                            </div>)}
                                    </Col>
                                </Row>
                            </Col>
                            <Col xs="auto">
                                <Row>
                                    <Col onClick={selectService}>
                                        <FontAwesomeIcon icon={faLinkedin} size="2x"
                                                         color={user.linkedin ? "#0072b1" : "gray"}/>
                                        {!user.reddit && (
                                            <div className="link-icon-container">
                                                <FontAwesomeIcon icon={faLinkedin} size="sm" color="black"/>
                                            </div>)}
                                    </Col>
                                </Row>
                            </Col>
                        </Row>
                    </Container>
                </Card.Body>
            </Card>
        </Container>
    )
        ;
};

export default SocialAccountsPostStatusBar;
