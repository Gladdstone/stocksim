import React, { Component } from 'react';
import { Button, Form } from 'react-bootstrap';

import './registration.less';

export default class Registration extends Component {

    render() {

        return (
            <div className='container'>
                <h2>Signup</h2>
                <Form>
                    <Form.Group controlId='formEmail'>
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type='email' placeholder='Enter email' />
                    </Form.Group>

                    <Form.Group controlId='formPassword'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type='password' placeholder='Password' />
                    </Form.Group>

                    <Button variant='primary' type='submit'>Signup</Button>
                </Form>
            </div>
        );

    }

}
