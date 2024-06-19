import React from "react";
import {Col, Container, Row} from "react-bootstrap";
import PostPanel from "../components/PostPanel.tsx";

const Dashboard: () => React.JSX.Element = () => {






    return (
        <Container>
            <Row>
                <Col>
                    <PostPanel/>
                </Col>
                <Col>
                    <h1>Services</h1>
                </Col>
            </Row>
        </Container>
    );
}

export default Dashboard; // Path: reposter-react/src/views/Users.tsx