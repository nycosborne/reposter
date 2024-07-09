import React from 'react';
import {Card, Container, Row, Col} from 'react-bootstrap';
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {useNavigate, useLocation} from "react-router-dom";
import SocialAccount from "./SocialAccount.tsx";
import {User} from "../types/types.tsx";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faLinkSlash} from "@fortawesome/free-solid-svg-icons";


interface SocialAccountsCardProps {
    showLink: boolean;
    user: User;
    // post: Post;
}

const SocialAccountsPostStatusBar = ({showLink, user}: SocialAccountsCardProps): React.JSX.Element => {


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
                                <Container>
                                    <Row>
                                        <Col onClick={selectService}>
                                            <FontAwesomeIcon icon={faRedditAlien} size="2x" color={user.reddit ? "#FF5700" : "gray"}/>
                                            {!user.reddit && (
                                                <div className="link-icon-container">
                                                    <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
                                                </div>)}
                                        </Col>
                                    </Row>
                                </Container>
                            </Col>
                            <Col xs="auto">
                                <SocialAccount
                                    isLinked={user.reddit}
                                    icon={faRedditAlien}
                                    color="#FF5700"
                                    accountStatusText="Reddit"
                                    handleLink={selectService}
                                    userAuthLink={''}
                                    showLink={showLink}
                                    isPostStatusBar={true}
                                />
                            </Col>
                            <Col xs="auto">
                                <SocialAccount
                                    isLinked={user.linkedin}
                                    icon={faLinkedin}
                                    color="#0072b1"
                                    accountStatusText="LinkedIn"
                                    handleLink={selectService}
                                    userAuthLink={''}
                                    showLink={showLink}
                                    isPostStatusBar={true}
                                />
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
