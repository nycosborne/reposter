import React, { useEffect } from 'react';
import { Card, ListGroup, Container } from 'react-bootstrap';
import useAppContext from "../context/UseAppContext.tsx";

const SocialAccountsCard = (): React.JSX.Element => {
    const {user, setUser} = useAppContext();
console.log('user', user)
    return (
        <Container>
            <Card>
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Social Accounts
                    </Card.Title>
                    <ListGroup>
                            {/*{posts.map(item => (*/}
                            {/*    <ListGroup.Item key={item.id}>*/}
                            {/*    <h6>{item.title}</h6>*/}
                            {/*    {location.pathname === '/dashboard' && <p>desc: {item.description}</p>}*/}
                            {/*    {location.pathname === '/posts' && <p>title: {item.content}</p>}*/}
                            {/*    {item.tags.map(tag => (*/}
                            {/*        <span key={tag.id}>tags: {tag.name}</span>*/}
                            {/*    ))}*/}
                            {/*</ListGroup.Item>*/}
                            {/*))}*/}
                        </ListGroup>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default SocialAccountsCard;
