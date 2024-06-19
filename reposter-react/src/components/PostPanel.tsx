import React, {useEffect} from 'react';
import {Row, Col, Card, ListGroup} from 'react-bootstrap';
import axiosClient from "../axios-clinet.tsx";


const PostPanel = (): React.JSX.Element => {

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

//useEffect to all the user/me endpoint to get the user details
useEffect(() => {
    axiosClient.get('/post/post/')
        .then((response) => {
            setPosts(response.data);
        })
        .catch((error) => {
            console.log('error', error);
        });
}, []); // eslint-disable-line react-hooks/exhaustive-deps
// todo fix the eslint warning

    return (
        <Row className="dashboard-panel-container">
            <Col>
                <Card>
                    <Card.Body>
                        <Card.Title as="h4" className="header">
                            <i className="fa fa-calendar"></i> Posts
                        </Card.Title>
                        <ListGroup>
                            <ListGroup.Item>
                                <i className="fa fa-plus-square">wqw</i>
                                <a data-turbo="false" className="calendar-name" href="/calendars/new">Add New
                                    Calendar</a>
                            </ListGroup.Item>
                            {posts.map(item => (
                                <ListGroup.Item key={item.id} className="calendar-item">
                                    <a className="calendar-name" href={item.link}>{item.title}</a>
                                </ListGroup.Item>
                            ))}
                        </ListGroup>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
    );
};

export default PostPanel;
