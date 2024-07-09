import React from 'react';
import {Row, Col, ListGroup, Container} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp } from '@fortawesome/fontawesome-svg-core';
import { faLinkSlash } from "@fortawesome/free-solid-svg-icons";

interface SocialAccountProps {
    isLinked: boolean;
    icon: IconProp;
    color: string;
    accountStatusText: string;
    handleLink: () => void;
    userAuthLink: string;
    showLink: boolean;
    isPostStatusBar?: boolean | undefined;
    isDashboard?: boolean | undefined;
}

const SocialAccount: React.FC<SocialAccountProps> = ({
    isLinked,
    icon,
    color,
    accountStatusText,
    handleLink,
    userAuthLink,
    showLink
}) => (
    // <ListGroup.Item action onClick={handleLink}>
    <Container>
        <Row>
            <Col onClick={handleLink}>
                <FontAwesomeIcon icon={icon} size="2x" color={isLinked ? color : "gray"}/>
                {!isLinked && (
                    <div className="link-icon-container">
                        <FontAwesomeIcon icon={faLinkSlash} size="sm" color="black"/>
                    </div>)}
            </Col>
            {/*<Col>*/}
            {/*    <h5>{accountStatusText}</h5>*/}
            {/*    <p>Account is: {isLinked ? "Linked" : "Unlinked"}</p>*/}
            {/*    {showLink && !isLinked && (*/}
            {/*        <a href={userAuthLink}>Link Account</a>*/}
            {/*    )}*/}
            {/*</Col>*/}
        </Row>
    </Container>
    // </ListGroup.Item>
);

export default SocialAccount;