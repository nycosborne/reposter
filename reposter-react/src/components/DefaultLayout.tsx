import React from 'react';
import {Outlet} from "react-router-dom";
import useAppContext from "../context/UseAppContext.tsx"
import {Col, Container, Row} from "react-bootstrap";

const DefaultLayout = (): React.JSX.Element => {

    const {token} = useAppContext();

    if (!token) {
        // return <Navigate to="/login"/>
    }

    return (
        <Container>
            <Row>
                <Col xs={"auto"}>
                    <h1>DefaultLayout</h1>
                    <Outlet/>
                </Col>
            </Row>
        </Container>
    )
}

export default DefaultLayout; // Path: reposter-react/src/components/DefaultLayout.tsx