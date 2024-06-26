import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import {Button} from "react-bootstrap";
import React, {useEffect} from "react";
import useAppContext from "../../context/UseAppContext.tsx";
import axiosClient from "../../axios-client.tsx";
import {Link} from "react-router-dom";

function NavBar() {

    const {user, setUser, setToken} = useAppContext();

    const logout = (ev: React.FormEvent) => {
        ev.preventDefault()
        setUser(null);
        setToken(null);
    }

    // useEffect to all the user/me endpoint to get the user details
    useEffect(() => {
        axiosClient.get('/user/me/')
            .then((response) => {
                setUser(response.data);
            })
            .catch((error) => {
                console.log('error', error);
            });
    }, []); // eslint-disable-line react-hooks/exhaustive-deps
    // todo fix the eslint warning


    return (
        <Navbar expand="lg" bg="dark" className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand as={Link} to="/">React-Bootstrap</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                {user &&
                    <Navbar.Text>
                        Hello {user.first_name}
                    </Navbar.Text>
                }
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/">Home</Nav.Link>
                        <Nav.Link as={Link} to="/compose">Compose Post</Nav.Link>
                    </Nav>
                    <Nav className="ml-auto">
                        <Button variant="outline-success" onClick={logout}>Logout</Button>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default NavBar;