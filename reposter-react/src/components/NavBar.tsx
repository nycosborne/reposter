import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
// import NavDropdown from 'react-bootstrap/NavDropdown';
import {Button} from "react-bootstrap";
import React, {useEffect} from "react";
import useAppContext from "../context/UseAppContext.tsx";
import axiosClient from "../axios-clinet.tsx";

function NavBar() {

    const {user, setUser, setToken} = useAppContext();
    const logout = (ev: React.FormEvent) => {
        ev.preventDefault()
        setUser(null);
        setToken(null);
    }


    // //useEffect to all the user/me endpoint to get the user details
    useEffect(() => {
        axiosClient.get('/user/me/')
            .then((response) => {
                setUser(response.data)
            })
            .catch((error) => {
                console.log('error', error)
            })
    }, [])

    if(user) {
       console.log('user', typeof user)
    }

    return (
        <Navbar expand="lg" bg="dark" className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                {user &&
                    <Navbar.Text>
                        Hello {user.first_name}
                    </Navbar.Text>
                }
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="#home">Home</Nav.Link>
                        <Nav.Link href="#link">Link</Nav.Link>
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