import React, {useEffect, useState} from 'react';
import {Col, Container, Row} from "react-bootstrap";
import {useLocation} from 'react-router-dom';

import PostPanel from "../components/PostPanel.tsx";
import SocialAccountsPanel from "../components/SocialAccountsPanel.tsx";

const Dashboard: () => React.JSX.Element = () => {

    const location = useLocation();
    const [key, setKey] = useState('');


    useEffect(() => {
        // Extract the query parameter or some part of the location to trigger a re-render
        const queryParams = new URLSearchParams(location.search);
        const updated = queryParams.get('updated');
        if (updated) {
            setKey(updated);
        }
    }, [location]);

    return (
        <Container>
            <Row>
                <Col>
                    <PostPanel/>
                </Col>
                <Col>
                    <SocialAccountsPanel showLink={false}/>
                </Col>
            </Row>
        </Container>
    );
}

export default Dashboard; // Path: reposter-react/src/views/Users.tsx