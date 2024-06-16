import React from 'react';
import {Outlet} from "react-router-dom";
import {Col, Container, Row} from "react-bootstrap";

const GuestLayout = (): React.JSX.Element => {
    return (
        <Container>
            <Row className="justify-content-md-center">
                <Col xs={"auto"}>
                    <Outlet/>
                </Col>
            </Row>
        </Container>

    )
}

export default GuestLayout; // Path: reposter-react/src/components/GuestLayout.tsx