import React from 'react';
import {Card, Container, Row, Col} from 'react-bootstrap';
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {useNavigate, useLocation} from "react-router-dom";
import SocialAccount from "./SocialAccount.tsx";
import {Post, User} from "../types/types.tsx";


interface SocialAccountsCardProps {
    showLink: boolean;
    user: User;
    post: Post;
}

const SocialAccountsPostStatusBar = ({showLink, user}: SocialAccountsCardProps): React.JSX.Element => {


    const navigate = useNavigate();
    const location = useLocation();


    const navigateToAccount = () => {
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
                                <SocialAccount
                                    isLinked={user.reddit}
                                    icon={faRedditAlien}
                                    color="#FF5700"
                                    accountStatusText="Reddit"
                                    handleLink={navigateToAccount}
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
                                    handleLink={navigateToAccount}
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
