import React from "react";
import {Col, Container, Row} from "react-bootstrap";
import SocialAccountsPanel from "../components/SocialAccountsPanel.tsx";

const AccountSettings: () => React.JSX.Element = () => {

    return (
        <Container>
            <Row>
                <Col>
                    AccountSettings
                    <SocialAccountsPanel showLink={true}/>
                </Col>
            </Row>
        </Container>
    );
}

export default AccountSettings; // Path: reposter-react/src/views/AccountSettings.tsx