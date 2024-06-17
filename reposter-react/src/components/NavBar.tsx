import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import {Button} from "react-bootstrap";
import React from "react";
import useAppContext from "../context/UseAppContext.tsx";

function NavBar() {

    const {setUser, setToken, token} = useAppContext();
    const logout = (ev: React.FormEvent) => {
        ev.preventDefault()
        setUser(null);
        setToken(null);
    }


    if (!token) {
        // return <Navigate to="/login"/>
    }

    return (
        <Navbar expand="lg" bg="dark" className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="#home">Home</Nav.Link>
                        <Nav.Link href="#link">Link</Nav.Link>
                        {/*<NavDropdown title="Dropdown" id="basic-nav-dropdown">*/}
                        {/*  <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>*/}
                        {/*  <NavDropdown.Item href="#action/3.2">*/}
                        {/*    Another action*/}
                        {/*  </NavDropdown.Item>*/}
                        {/*  <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>*/}
                        {/*  <NavDropdown.Divider />*/}
                        {/*  <NavDropdown.Item href="#action/3.4">*/}
                        {/*    Separated link*/}
                        {/*  </NavDropdown.Item>*/}
                        {/*</NavDropdown>*/}
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