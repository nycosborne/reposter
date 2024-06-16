import React from 'react';
import {Outlet} from "react-router-dom";
import useAppContext from "../context/UseAppContext.tsx"
import {Button, Col, Container, Row} from "react-bootstrap";

const DefaultLayout = (): React.JSX.Element => {

    const {user, token} = useAppContext();

    if (!token) {
        // return <Navigate to="/login"/>
    }

    const logout = (ev: React.FormEvent) => {
        ev.preventDefault()
        // setUser(null);
        // setToken(null);
    }

    // @ts-ignore
    return (
        <Container>
            <Row>
                <Col xs={"auto"}>
                    {user.name}
                    <Button onClick={logout}>LogOut</Button>
                    <h1>DefaultLayout</h1>
                    <Outlet/>
                </Col>
            </Row>
        </Container>
    )
}

export default DefaultLayout; // Path: reposter-react/src/components/DefaultLayout.tsx