import React from 'react';
import {Navigate, Outlet} from "react-router-dom";
import {Col, Container, Row} from "react-bootstrap";
import useAppContext from "../context/UseAppContext.tsx";

const GuestLayout = (): React.JSX.Element => {

    const {token} = useAppContext();

    if (token) {
        return <Navigate to='/'/>
    }


    return (
        <Container fluid className="d-flex justify-content-center align-items-center" style={{ minHeight: "90vh" }}>
            <Row>
                <Col xs={"auto"}>
                    <Outlet/>
                </Col>
            </Row>
        </Container>

    )
}

export default GuestLayout; // Path: reposter-react/src/components/GuestLayout.tsx