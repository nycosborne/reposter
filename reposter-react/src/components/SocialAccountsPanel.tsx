import React from 'react';
import {Card, ListGroup, Container, Row} from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faLinkSlash} from "@fortawesome/free-solid-svg-icons";

const SocialAccountsCard = (): React.JSX.Element => {
    const {user} = useAppContext();

    if (!user) {
        return <div>Loading...</div>
    }

    return (
        <Container>
            <Card>
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Social Accounts Status
                    </Card.Title>
                    {user &&
                        <ListGroup>
                            <ListGroup.Item>
                                {user && user.reddit ?
                                    <FontAwesomeIcon icon={faRedditAlien} size="2x" color="#FF5700"/> :
                                    <Row>
                                        <FontAwesomeIcon icon={faRedditAlien} size="2x" color="gray"/>
                                        <div className={"link-icon-container"}>
                                            <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
                                        </div>
                                            <p>Reddit Unlinked</p>
                                    </Row>
                                }
                            </ListGroup.Item>
                            <ListGroup.Item>
                                {user && user.linkedin ?
                                    <FontAwesomeIcon icon={faLinkedin} size="2x" color="#0072b1"/> :
                                    <Row>
                                        <FontAwesomeIcon icon={faLinkedin} size="2x" color="gray"/>
                                        <div className={"link-icon-container"}>
                                            <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
                                        </div>
                                        <p>LinkedIn Unlinked</p>
                                    </Row>
                                }
                            </ListGroup.Item>
                        </ListGroup>
                    }
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsCard;
