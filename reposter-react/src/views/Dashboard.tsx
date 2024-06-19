import React from "react";
import {Container} from "react-bootstrap";

const Dashboard: () => React.JSX.Element = () => {

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{minHeight: "90vh"}}>
            <h1>Posts</h1>
        </Container>
    );
}

export default Dashboard; // Path: reposter-react/src/views/Users.tsx