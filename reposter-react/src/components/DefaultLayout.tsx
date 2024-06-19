import React from 'react';
import {Navigate, Outlet} from "react-router-dom";
import Navbar from "./ui/NavBar.tsx";
import useAppContext from "../context/UseAppContext.tsx"
import {Container} from "react-bootstrap";

const DefaultLayout = (): React.JSX.Element => {

    const {token} = useAppContext();

    if (!token) {
        return <Navigate to="/login"/>
    }

    return (
        <>
            <Navbar/>
            <h1>DefaultLayout</h1>
            <Container fluid className="d-flex justify-content-center align-items-center" style={{minHeight: "90vh"}}>
                <Outlet/>
            </Container>
        </>
    )
}

export default DefaultLayout; // Path: reposter-react/src/components/DefaultLayout.tsx