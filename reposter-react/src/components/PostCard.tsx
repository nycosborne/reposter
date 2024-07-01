import React, {useEffect} from 'react';
import {Card, ListGroup, Container} from 'react-bootstrap';
import axiosClient from "../axios-client.tsx";
import { Link } from 'react-router-dom';

interface PostCardProps {
    dashboard?: boolean
}

const PostCard = ({dashboard}: PostCardProps): React.JSX.Element => {

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
                                {dashboard ? (
                                    <Link to={`/compose/${item.id}`}>
                                        <h6>{item.title}</h6>
                                        <p>desc: {item.description}</p>
                                    </Link>
                                ) : (
                                    <>
                                        <h6>{item.title}</h6>
                                        <p>title: {item.content}</p>
                                    </>
                                )}
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
