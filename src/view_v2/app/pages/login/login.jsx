import React, { Component } from 'react';
import { Button, Form } from 'react-bootstrap';

import './login.less';

export default class Login extends Component {

    render() {

        return (
            <div className='container'>
                <h2>Login</h2>
                <Form>
                    <Form.Group controlId='formEmail'>
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type='email' placeholder='Enter email' />
                    </Form.Group>

                    <Form.Group controlId='formPassword'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type='password' placeholder='Password' />
                    </Form.Group>

                    <Button variant='primary' type='submit'>Submit</Button>
                </Form>
            </div>
        );

    }

}
