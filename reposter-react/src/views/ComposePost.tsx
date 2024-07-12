import React, {useEffect, useState} from 'react';
import {Button, Form} from 'react-bootstrap';
import axiosClient from "../axios-client.tsx";
import {useNavigate, useParams} from "react-router-dom";
import SocialAccountsPostStatusBar from "../components/ui/SocialAccountsPostStatusBar.tsx";


const ComposePost: React.FC = () => {
    const navigate = useNavigate();

    interface Tag {
        id: number;
        name: string;
    }

    interface ServiceRequested {
        id?: number;
        post_id?: number;
        service: string;
        status: string;
    }

    interface Post {
        id?: number;
        title?: string;
        content: string;
        description?: string;
        link?: string;
        tags?: Tag[];
        status: string;
        image?: string | null;
        service_requested?: ServiceRequested[];
        post_service_events?: ServiceRequested[];
    }

    const [post, setPost] = useState<Post>({
        title: '',
        description: '',
        content: '',
        status: 'DRAFT',
        service_requested: []
    });

    const [selectedReddit, setSelectedReddit] = useState<string>('');
    const [selectedLinkedin, setSelectedLinkedin] = useState<string>('');

    const selectReddit = (service: string) => {
        setSelectedReddit(prevService => prevService === service ? '' : service); // Toggle service selection
    };
    const selectLinkedin = (service: string) => {
        setSelectedLinkedin(prevService => prevService === service ? '' : service); // Toggle service selection
    };

    const {post_id} = useParams();
    useEffect(() => {
        if (post_id) {
            axiosClient.get(`/post/post/${post_id}`)
                .then(({data}) => {
                    console.log('data', data);
                    // console.log('checkServices :', checkServices(data));
                    setPost(data);
                    // Check if data has post_service_events
                    if (data.post_service_events && Array.isArray(data.post_service_events)) {
                        console.log('data.post_service_events', data.post_service_events);
                        // Loop over the post_service_events array
                        data.post_service_events.forEach(function (event: { service: string; status: React.SetStateAction<string>; }) {
                            console.log('event', event);
                            if (event.service === 'reddit') {
                                setSelectedReddit('reddit');
                            } else if (event.service === 'linkedin') {
                                setSelectedLinkedin('linkedin');
                            }
                        });
                    }
                    // check data if it has post_service_events and if service === reddit or linkedin
                });

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

    const createServiceRequested = (status?: string): ServiceRequested[] => {
        const services: { service: string; status: string }[] = [];
        if (selectedReddit) {
            services.push({service: 'reddit', status: status ? status : 'PENDING'});
        }
        if (selectedLinkedin) {
            services.push({service: 'linkedin', status: status ? status : 'PENDING'});
        }
        return services;
    };

    const savePost = async (event: React.FormEvent) => {
        event.preventDefault();

        const payload = {
            title: post.title || "",
            description: post.description || "",
            content: post.content || "",
            link: "", // Assuming you have a link to include or it can be an empty string if not
            tags: [], // Assuming you have tags to include or it can be an empty array if not
            // TODO need to standrdize the service_requested and post_service_events
            service_requested: createServiceRequested('PENDING'),
            status: post.status || "DRAFT",
        };


        if (post_id) {
            axiosClient.put(`/post/post/${post_id}/`, payload, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
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
                console.log('Successfully created new Post', response);
                navigate(`/compose/${response.data.id}`);
            })
            .catch((error) => {
                console.log('error', error);
            });
    };

    const postToSocialMedia = async (event: React.FormEvent) => {
        event.preventDefault();
        // const payload: {
        //     title: string,
        //     description: string,
        //     content: string,
        //     post_id: string,
        //     social_accounts: string
        // } = {
        //     title: post.title ? post.title : "",
        //     description: post.description ? post.description : "",
        //     content: post.content ? post.content : "",
        //     post_id: post_id ? post_id : "",
        //     social_accounts: 'reddit'
        // };

        const payload: Post = {
            id: post_id ? parseInt(post_id) : undefined,
            title: post.title || "",
            description: post.description || "",
            content: post.content || "",
            link: "", // Assuming you have a link to include or it can be an empty string if not
            tags: [], // Assuming you have tags to include or it can be an empty array if not
            post_service_events: createServiceRequested('SET_TO_PUBLISH'),
            status: post.status || "DRAFT",
        };

        console.log('payload', payload);
        axiosClient.post('/services/soc-post/', payload)
            .then((response) => {
                console.log('Posted successfully', response);
                navigate(`/compose/${post_id}`);
            })
            .catch((error) => {
                console.log('error 2@#$@#$@#$', error);
            });
    };

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
            <SocialAccountsPostStatusBar
                // selectReddit={selectReddit}
                selectReddit={selectReddit}
                selectedReddit={selectedReddit}
                selectLinkedin={selectLinkedin}
                selectedLinkedin={selectedLinkedin}
                postData={post}/>
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