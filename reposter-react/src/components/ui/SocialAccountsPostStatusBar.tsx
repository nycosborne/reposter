import React, {useState} from 'react';
import {Card, Container, Row, Col} from 'react-bootstrap';
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

interface SocialAccountsIcons {
    reddit: boolean;
    linkedin: boolean;
}

interface SocialAccountsPostStatusBarProps {
    icons: SocialAccountsIcons;
}

const SocialAccountsPostStatusBar = ({icons}: SocialAccountsPostStatusBarProps): React.JSX.Element => {
    const [selectedReddit, setSelectedReddit] = useState<string>('');
    const [selectedLinkedin, setSelectedLinkedin] = useState<string>('');

    const selectReddit = (service: string) => {
        setSelectedReddit(prevService => prevService === service ? '' : service); // Toggle service selection
    }

    const selectLinkedin = (service: string) => {
        setSelectedLinkedin(prevService => prevService === service ? '' : service); // Toggle service selection
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
                                    <Col onClick={() => selectReddit('reddit')}>
                                        <FontAwesomeIcon icon={faRedditAlien} size="2x"
                                                         color={selectedReddit === 'reddit' ? "#FF5700" : "gray"}/>
                                    </Col>
                                </Row>
                            </Col>
                            <Col xs="auto">
                                <Row>
                                    <Col onClick={() => selectLinkedin('linkedin')}>
                                        <FontAwesomeIcon icon={faLinkedin} size="2x"
                                                         color={selectedLinkedin === 'linkedin' ? "#0072b1" : "gray"}/>
                                    </Col>
                                </Row>
                            </Col>
                        </Row>
                    </Container>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsPostStatusBar;