import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Card, ListGroup, Container } from 'react-bootstrap';
import axiosClient from "../axios-clinet.tsx";

const PostCard = (): React.JSX.Element => {

    const location = useLocation();

    interface Tag {
        id: number;
        name: string;
    }

    interface ListPost {
        id: number;
        title: string;
        content: string;
        description: string;
        link: string;
        tags: Tag[];
    }

    const [posts, setPosts] = React.useState<ListPost[]>([]);

    // useEffect to call the /post/post/ endpoint to get the post details
    useEffect(() => {
        axiosClient.get('/post/post/')
            .then((response) => {
                setPosts(response.data);
            })
            .catch((error) => {
                console.log('error', error);
            });
    }, []);

    return (
        <Container>
            <Card>
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Posts
                    </Card.Title>
                    <ListGroup>
                            {posts.map(item => (
                                <ListGroup.Item key={item.id}>
                                <h6>{item.title}</h6>
                                {location.pathname === '/dashboard' && <p>desc: {item.description}</p>}
                                {location.pathname === '/posts' && <p>title: {item.content}</p>}
                                {item.tags.map(tag => (
                                    <span key={tag.id}>tags: {tag.name}</span>
                                ))}
                            </ListGroup.Item>
                            ))}
                        </ListGroup>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default PostCard;
