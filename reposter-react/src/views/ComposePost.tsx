import React, { useState } from 'react';
import { Button, Form } from 'react-bootstrap';

const ComposePost: React.FC = () => {
    const [postContent, setPostContent] = useState('');

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        // Here you can handle the submission of the post content
        console.log(postContent);
    };

    return (
        <Form onSubmit={handleSubmit}>
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