import React, {useState} from 'react';
import {Button, Form} from 'react-bootstrap';
import axiosClient from "../axios-client.tsx";

const ComposePost: React.FC = () => {
    const [postTitle, setPostTitle] = useState('');
    const [postDescription, setPostDescription] = useState('');
    const [postContent, setPostContent] = useState('');

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        const payload: { title: string, description: string, content: string } = {
            title: postTitle ? postTitle : "",
            description: postDescription ? postDescription : "",
            content: postContent ? postContent : "",
        };

        axiosClient.post('/post/post/', payload)
            .then((response) => {
                console.log('Posted successfully', response);
            })
            .catch((error) => {
                console.log('error', error);
            });
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
                <Form.Label>Title</Form.Label>
                <Form.Control
                    type="text"
                    value={postTitle}
                    onChange={e => setPostTitle(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Description</Form.Label>
                <Form.Control
                    type="text"
                    value={postDescription}
                    onChange={e => setPostDescription(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Compose Post</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    value={postContent}
                    onChange={e => setPostContent(e.target.value)}
                />
            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
    );
};

export default ComposePost;