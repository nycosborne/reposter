import React from 'react';
import {Row, Col} from 'react-bootstrap';
import PostCard from "./PostCard.tsx";


const PostPanel = (): React.JSX.Element => {

    return (
        <Row >
            <Col>
                <PostCard dashboard={true} />
            </Col>
        </Row>
    );
};

export default PostPanel;
