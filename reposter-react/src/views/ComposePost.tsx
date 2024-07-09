import React, {useEffect, useState} from 'react';
import {Button, Form} from 'react-bootstrap';
import axiosClient from "../axios-client.tsx";
import {useNavigate, useParams} from "react-router-dom";
import SocialAccountsPostStatusBar from "../components/ui/SocialAccountsPostStatusBar.tsx";
import useAppContext from "../context/UseAppContext.tsx";
import {User} from "../components/types/types.tsx";

const ComposePost: React.FC = () => {

    const {user} = useAppContext();

    const navigate = useNavigate();

    interface Post {
        title: string;
        description: string;
        content: string;
        status: string;
        user?: User | null;
    }

    const [post, setPost] = useState<Post>(
        {
            title: '',
            description: '',
            content: '',
            status: 'DRAFT'
        }
    );

    const [selectedReddit, setSelectedReddit] = useState<string>('');
    const [selectedLinkedin, setSelectedLinkedin] = useState<string>('');

    const selectReddit = (service: string) => {
        setSelectedReddit(prevService => prevService === service ? '' : service); // Toggle service selection
    }
    const selectLinkedin = (service: string) => {
        setSelectedLinkedin(prevService => prevService === service ? '' : service); // Toggle service selection
    }
    let icons = {reddit: false, linkedin: false}; // Initialize with default values
    if (user) {
        icons = {
            reddit: user.reddit,
            linkedin: user.linkedin,
        };
    }


    const {post_id} = useParams();
    useEffect(() => {
        if (post_id) {
            // Get request with post_slug and arg
            axiosClient.get(`/post/post/${post_id}`)
                .then(({data}) => {
                    console.log('data', data);
                    setPost(data);
                })
        }
    }, [post_id]);

    const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPost(prevState => ({...prevState, title: e.target.value}));
    };

    const handleDescriptionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPost(prevState => ({...prevState, description: e.target.value}));
    };

    const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setPost(prevState => ({...prevState, content: e.target.value}));
    };

    const savePost = async (event: React.FormEvent) => {
        event.preventDefault();
        // Assuming selectedReddit and selectedLinkedin are correctly set to 'reddit' or 'linkedin' when selected
        const serviceRequested = [];
        if (selectedReddit) {
            serviceRequested.push({service: 'reddit', status: 'PENDING'});
        }
        if (selectedLinkedin) {
            serviceRequested.push({service: 'linkedin', status: 'PENDING'});
        }

        const payload = {
            title: post.title || "",
            description: post.description || "",
            content: post.content || "",
            link: "",
            service_requested: serviceRequested,
            status: post.status || "DRAFT",
        };

        console.log('payload', payload);
        if (post_id) {
            axiosClient.put(`/post/post/${post_id}/`, payload)
                .then((response) => {
                    console.log('Updated successfully', response);
                    navigate(`/compose/${response.data.id}`);
                })
                .catch((error) => {
                    console.log('error', error);
                });
            return;
        }
        axiosClient.post('/post/post/', payload)
            .then((response) => {
                console.log('Posted successfully', response);
                navigate(`/compose/${response.data.id}`);
            })
            .catch((error) => {
                console.log('error', error);
            });

    };

    const postToSocialMedia = async (event: React.FormEvent) => {
        event.preventDefault();
        const payload: {
            title: string,
            description: string,
            content: string,
            post_id: string,
            social_accounts: string
        } = {
            title: post.title ? post.title : "",
            description: post.description ? post.description : "",
            content: post.content ? post.content : "",
            post_id: post_id ? post_id : "",
            // TODO: Need to set the social account from new modal
            social_accounts: 'reddit'
        };

        axiosClient.post('/services/soc-post/', payload)
            .then((response) => {
                console.log('Posted successfully', response);
                navigate(`/compose/${post_id}`);
            })
            .catch((error) => {
                console.log('error 2@#$@#$@#$', error);
            });
    }

    return (
        <Form onSubmit={savePost}>
            <Form.Label>Status : {post.status}</Form.Label>
            <Form.Group className="mb-3">
                <Form.Label>Title</Form.Label>
                <Form.Control
                    type="text"
                    value={post.title}
                    onChange={handleTitleChange}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Description</Form.Label>
                <Form.Control
                    type="text"
                    value={post.description}
                    onChange={handleDescriptionChange}
                />
            </Form.Group>
            <SocialAccountsPostStatusBar icons={icons}
                                         selectReddit={selectReddit}
                                         selectedReddit={selectedReddit}
                                         selectLinkedin={selectLinkedin}
                                         selectedLinkedin={selectedLinkedin}/>

            <Form.Group className="mb-3">
                <Form.Label>Compose Post</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    value={post.content}
                    onChange={handleContentChange}
                />
            </Form.Group>
            <Button variant="primary" type="submit">
                Save Post
            </Button>
            <span> | </span>
            <Button variant="primary" onClick={postToSocialMedia}>
                Post To Social Media
            </Button>
        </Form>
    );
};

export default ComposePost;