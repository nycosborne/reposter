import React, {createRef, RefObject} from 'react';
import {Form, Button} from "react-bootstrap";
import useAppContext from "../context/UseAppContext.tsx";
import axiosClient from "../axios-client.tsx";
import {AxiosResponse} from "axios";
import {Link} from "react-router-dom";

const Login = (): React.JSX.Element => {

    const emailRef: RefObject<HTMLInputElement> = createRef();
    const passwordRef: RefObject<HTMLInputElement> = createRef()

    const [error, setErrors] = React.useState<string | null>(null);
    const {setToken} = useAppContext();

    interface LoginResponse {
        token: string;
    }


    const logIn = (ev: React.FormEvent) => {
        ev.preventDefault();


        const payload: { email: string, password: string } = {
            email: emailRef.current ? emailRef.current.value : "",
            password: passwordRef.current ? passwordRef.current.value : ""
        };

        axiosClient.post<LoginResponse>('/user/token/', payload)
            .then((response: AxiosResponse<LoginResponse>) => {
                const data = response.data;
                setToken(data.token)
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
        <Form onSubmit={logIn} className={'animated fadeInDown'}>
            <h1>Log In</h1>
            {error && <div style={{background: "lightpink"}}>
                {error}
            </div>}
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Control ref={emailRef} type="email" placeholder="Enter email"/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Control ref={passwordRef} type="password" placeholder="Password"/>
            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
            <p className="message"><Link to="/signup">Create an account</Link></p>
            {/*<p className="message">Not registered? <Link to="/signup">Create an account</Link></p>*/}
        </Form>
    )
}

export default Login; // Path: reposter-react/src/views/Users.tsx