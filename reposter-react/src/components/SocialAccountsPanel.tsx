import React, { useEffect } from 'react';
import { Card, ListGroup, Container } from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";

const SocialAccountsCard = (): React.JSX.Element => {
    const {user, setUser} = useAppContext();

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <Container>
            <Card>
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Social Accounts
                    </Card.Title>
                    {user.linkedin &&
                        <ListGroup>
                            <ListGroup.Item>
                                LinkedIn
                            </ListGroup.Item>
                        </ListGroup>
                    }
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsCard;
