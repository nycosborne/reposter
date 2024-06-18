import React, {createRef, RefObject} from 'react'
import {Button, Form} from "react-bootstrap";
import axiosClient from "../axios-clinet.tsx";
import {AxiosResponse} from "axios";


const Signup: () => React.JSX.Element = () => {

    const firstNameRef: RefObject<HTMLInputElement> = createRef();
    const lastNameRef: RefObject<HTMLInputElement> = createRef();
    const emailRef: RefObject<HTMLInputElement> = createRef();
    const passwordRef: RefObject<HTMLInputElement> = createRef()
    const passwordConfirRef: RefObject<HTMLInputElement> = createRef()

    // const timeZoneRef: RefObject<HTMLInputElement> = createRef()

    interface CreateAccountResponse {
        email: string;
        firstName: string;
        lastName: string;
    }


    const [error, setErrors] = React.useState<string | null>(null);

    const checkPasswordIdentical = (password: string, passwordConfirm: string) => {
        if (password !== passwordConfirm) {
            setErrors("Passwords do not match")
        }
    }
    const signUp = (ev: React.FormEvent) => {
        ev.preventDefault();

        checkPasswordIdentical(passwordRef.current ? passwordRef.current.value : "",
            passwordConfirRef.current ? passwordConfirRef.current.value : "")

        const payload: { firstName: string, lastName: string, email: string, password: string } = {
            firstName: firstNameRef.current ? firstNameRef.current.value : "",
            lastName: lastNameRef.current ? lastNameRef.current.value : "",
            email: emailRef.current ? emailRef.current.value : "",
            password: passwordRef.current ? passwordRef.current.value : ""
        };

        axiosClient.post<CreateAccountResponse>('/user/create/', payload)
            .then((response: AxiosResponse<CreateAccountResponse>) => {
                const data = response.data;
                console.log('response', data)
            })
            .catch((error) => {
                const errorMessage = error.response
                if (errorMessage && errorMessage.status === 403) {
                    if (errorMessage.data.detail) {
                        setErrors(errorMessage.data.detail)
                    }
                }
            })
    }


    return (
        <Form onSubmit={signUp} className={'animated fadeInDown'}>
            <h1>Sign Up</h1>
            {error && <div style={{background: "lightgray"}}>
                {error}
            </div>}

            <Form.Group className="mb-3" controlId="formBasicName">
                <Form.Label>First Name</Form.Label>
                <Form.Control ref={firstNameRef} type="text" placeholder="First Name"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicName">
                <Form.Label>Last Name</Form.Label>
                <Form.Control ref={lastNameRef} type="text" placeholder="Last Name"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control ref={emailRef} type="email" placeholder="Enter email"/>
                <Form.Text className="text-muted">
                    We'll never share your email with anyone else.
                </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control ref={passwordRef} type="password" placeholder="Password"/>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control ref={passwordConfirRef} type="password" placeholder="Password"/>
            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
            {/*Will uncomment when I have multiple uses support*/}
            {/*<p className="message">Not registered? <Link to="/signup">Create an account</Link></p>*/}
            {/*<p className="message">Forgot Password<Link to="/signup">Create an account</Link></p>*/}
        </Form>
    )
}

export default Signup; // Path: reposter-react/src/views/Signup.tsx