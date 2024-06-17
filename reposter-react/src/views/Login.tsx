import React, {createRef, RefObject} from 'react';
import {Form, Button} from "react-bootstrap";
import useAppContext from "../context/UseAppContext.tsx";
import axiosClient from "../axios-clinet.tsx";
import {AxiosResponse} from "axios";

const Login = (): React.JSX.Element => {

    const emailRef: RefObject<HTMLInputElement> = createRef();
    const passwordRef: RefObject<HTMLInputElement> = createRef()

    // const [errors, setErrors: ] = useState([])
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
                const response = error.response
                console.log('response', response)
                // if (response && response.status === 422) {
                //     if(response.data.error) {
                //         setErrors(response.data.errors)
                //     }else {
                //         setErrors({
                //             error: [response.data.message]
                //         })
                //     }
                // }
            })

    }

    return (
        <Form onSubmit={logIn} className={'animated fadeInDown'}>
            <h1>Log In</h1>
            <Form.Group className="mb-3" controlId="formBasicEmail">

                {/*{errors && <div style={{background: "lightpink"}}>*/}
                {/*    <ul>*/}
                {/*        {Object.keys(errors).map(key => (*/}
                {/*            <li key={key}>{errors[key][0]}</li>*/}
                {/*        ))*/}
                {/*        }*/}
                {/*    </ul>*/}
                {/*</div>*/}
                {/*}*/}
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
            <Button variant="primary" type="submit">
                Submit
            </Button>
            {/*Will uncomment when I have multiple uses support*/}
            {/*<p className="message">Not registered? <Link to="/signup">Create an account</Link></p>*/}
        </Form>
    )
}

export default Login; // Path: reposter-react/src/views/Users.tsx