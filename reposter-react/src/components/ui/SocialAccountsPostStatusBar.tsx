import React from 'react';
import { Card, Container, Row, Col } from 'react-bootstrap';
import { faLinkedin, faRedditAlien } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface SocialAccountsPostStatusBarProps {
    selectReddit: (service: string) => void;
    selectedReddit: string;
    selectedLinkedin: string;
    selectLinkedin: (service: string) => void;
}

const SocialAccountsPostStatusBar = ({
    selectReddit,
    selectedReddit,
    selectedLinkedin,
    selectLinkedin,
}: SocialAccountsPostStatusBarProps): React.JSX.Element => {

    return (
        <Container className="d-flex justify-content-center w-100">
            <Card className="post-card-panel">
                <Card.Body>
                    <Card.Title as="h5" className="header">
                        Select Platforms
                    </Card.Title>
                    <Container>
                        <Row className="align-items-center justify-content-center">
                            <Col xs="auto" className="text-center">
                                <Row>
                                    <Col onClick={() => selectReddit('reddit')}>
                                        <FontAwesomeIcon
                                            icon={faRedditAlien}
                                            size="2x"
                                            color={selectedReddit ? "#FF5700" : "gray"}
                                        />
                                    </Col>
                                </Row>
                            </Col>
                            <Col xs="auto" className="text-center">
                                <Row>
                                    <Col onClick={() => selectLinkedin('linkedin')}>
                                        <FontAwesomeIcon
                                            icon={faLinkedin}
                                            size="2x"
                                            color={selectedLinkedin ? "#0072b1" : "gray"}
                                        />
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
