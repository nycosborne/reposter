import React from 'react';
import {Outlet} from "react-router-dom";
import {Container} from "react-bootstrap";

const GuestLayout = (): React.JSX.Element => {
    return (
        <Container>
            <Outlet/>
        </Container>
    )
}

export default GuestLayout; // Path: reposter-react/src/components/GuestLayout.tsx