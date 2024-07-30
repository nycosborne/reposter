import React, { useEffect } from 'react';
import { Card, ListGroup, Container, Row, Col } from 'react-bootstrap';
import axiosClient from "../axios-client.tsx";
import { Link } from 'react-router-dom';

interface PostCardProps {
    dashboard?: boolean;
}

const PostCard = ({ dashboard }: PostCardProps): React.JSX.Element => {

    interface Tag {
        id: number;
        name: string;
    }

    interface ListPost {
        id: number;
        status: string;
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

    const formatStatus = (status: string): string => {
        return status.charAt(0).toUpperCase() + status.slice(1).toLowerCase();
    };

    return (
        <Container>
            <Card className="dashboard-panel">
                <Card.Body>
                    <Card.Title as="h4" className="header">
                        Posts
                    </Card.Title>
                    <ListGroup>
                        {posts.map(item => (
                            <ListGroup.Item key={item.id}>
                                <Container>
                                    {dashboard ? (
                                        <Row>
                                            <Col>
                                                <Link to={`/compose/${item.id}`}>
                                                    <h6>{item.title}</h6>
                                                    <p>desc: {item.description}</p>
                                                </Link>
                                            </Col>
                                            <Col>
                                                <p>Status: {formatStatus(item.status)}</p>
                                            </Col>
                                        </Row>
                                    ) : (
                                        <>
                                            <h6>{item.title}</h6>
                                            <p>title: {item.content}</p>
                                        </>
                                    )}
                                    {item.tags.map(tag => (
                                        <span key={tag.id}>tags: {tag.name}</span>
                                    ))}
                                </Container>
                            </ListGroup.Item>
                        ))}
                    </ListGroup>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default PostCard;
