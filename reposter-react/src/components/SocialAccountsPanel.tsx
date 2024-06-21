import React from 'react';
import { Card, ListGroup, Container } from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";

const SocialAccountsCard = (): React.JSX.Element => {
    const {user} = useAppContext();

    if(!user) {
        return <div>Loading...</div>
    }

    return (
        <Container>
            <Card>
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Social Accounts
                    </Card.Title>
                    <ListGroup>
                        {user.linkedin &&
                            <ListGroup.Item>
                                {user.first_name}
                            </ListGroup.Item>
                        }
                        </ListGroup>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsCard;
