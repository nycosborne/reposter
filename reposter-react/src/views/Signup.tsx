import React, {createRef, RefObject} from 'react'
import {Button, Form} from "react-bootstrap";
import axiosClient from "../axios-clinet.tsx";
import {Navigate} from 'react-router-dom';


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

    interface Errors {
        [key: string]: string[];
    }

    const [shouldRedirect, setShouldRedirect] = React.useState(false);
    const [error, setErrors] = React.useState<Errors>({});

    const checkPasswordIdentical = (password: string, passwordConfirm: string) => {
        if (password !== passwordConfirm) {
            setErrors({password: ['Passwords do not match']});
        }
    }
    const signUp = (ev: React.FormEvent) => {
        ev.preventDefault();

        checkPasswordIdentical(passwordRef.current ? passwordRef.current.value : "",
            passwordConfirRef.current ? passwordConfirRef.current.value : "")

        const payload: { first_name: string, last_name: string, email: string, password: string } = {
            first_name: firstNameRef.current ? firstNameRef.current.value : "",
            last_name: lastNameRef.current ? lastNameRef.current.value : "",
            email: emailRef.current ? emailRef.current.value : "",
            password: passwordRef.current ? passwordRef.current.value : ""
        };

        axiosClient.post<CreateAccountResponse>('/user/create/', payload)
            .then(() => {
                setShouldRedirect(true)
            })
            .catch((error) => {
                const errorResponse = error.response
                if (errorResponse && errorResponse.status === 400) {
                    if (errorResponse.data) {
                        setErrors(errorResponse.data)
                    }
                }
            })
    }

    console.log('error', error)
    if (shouldRedirect) {
        return <Navigate to="/login"/>
    }

    return (
        <Form onSubmit={signUp} className={'animated fadeInDown'}>
            <h1>Sign Up</h1>
            {Object.keys(error).length > 0 && (
                <div style={{background: "lightpink"}}>
                    <ul>
                        {Object.keys(error).map((key) => (
                            <li key={key}>{key}: {error[key][0]}</li>
                        ))}
                    </ul>
                </div>
            )}

            <Form.Group className="mb-3" controlId="formBasicName">
                <Form.Control ref={firstNameRef} type="text" placeholder="First Name"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicName">
                <Form.Control ref={lastNameRef} type="text" placeholder="Last Name"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Control ref={emailRef} type="email" placeholder="Enter email"/>
                <Form.Text className="text-muted">
                    We'll never share your email with anyone else.
                </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Control ref={passwordRef} type="password" placeholder="Password"/>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
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