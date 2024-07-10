import React from 'react';
import {Card, Container, Row, Col} from 'react-bootstrap';
import {faLinkedin, faRedditAlien} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Post} from "../types/types.tsx";

interface SocialAccountsIcons {
    reddit: boolean;
    linkedin: boolean;
}

interface SocialAccountsPostStatusBarProps {
    icons: SocialAccountsIcons;
    selectReddit: (service: string) => void;
    selectedReddit: string;
    selectedLinkedin: string;
    selectLinkedin: (service: string) => void;
    postData: Post;
}

const SocialAccountsPostStatusBar = ({
                                         selectReddit,
                                         selectedReddit,
                                         selectedLinkedin,
                                         selectLinkedin,
                                         postData
                                     }: SocialAccountsPostStatusBarProps): React.JSX.Element => {
    postData.post_service_events && postData.post_service_events.map((event, index) => (
        // console.log('index', postData.post_service_events[index])
        console.log('index', event.service),
            console.log('index', event.service)
        // console.log('event', event)
        // <div key={index}>
        //     <p>Service: {event.service}</p>
        //     <p>Status: {event.status}</p>
        // </div>
    ))

    if (postData.post_service_events) {
        const newArray = postData.post_service_events.map((event, index) => {
            // Modify this return statement as needed for your specific use case
            if(event.service){

            }
            return {
                service: event.service,
                status: event.status,
            };
        });

        // newArray now holds the transformed array
        // Use newArray as needed in your application
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
                                                         color={selectedReddit ? "#FF5700" : "gray"}/>
                                    </Col>
                                </Row>
                            </Col>
                            <Col xs="auto">
                                <Row>
                                    <Col onClick={() => selectLinkedin('linkedin')}>
                                        <FontAwesomeIcon icon={faLinkedin} size="2x"
                                                         color={selectedLinkedin ? "#0072b1" : "gray"}/>
                                    </Col>
                                </Row>
                            </Col>
                        </Row>
                        {/*/!* Render service events *!/*/}
                        {/*{postData.post_service_events && postData.post_service_events.map((event, index) => (*/}
                        {/*    <div key={index}>*/}
                        {/*        <p>Service: {event.service}</p>*/}
                        {/*        <p>Status: {event.status}</p>*/}
                        {/*    </div>*/}
                        {/*))}*/}
                    </Container>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsPostStatusBar;