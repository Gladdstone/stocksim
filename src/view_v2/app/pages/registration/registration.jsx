import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, Form } from 'react-bootstrap';

import { userPostRegistration } from '../../modules/actions';

import './registration.less';
class Registration extends Component {

    constructor(props) {

        super(props);
        this.state = {
            email: '',
            password: ''
        };

    }

    handleFormUpdate = event => {

        this.setState({
            [event.target.name]: event.target.value
        });

    }

    handleSubmit = event => {

        this.props.userPostRegistration(this.state);

    }

    render() {

        return (
            <div className='container'>
                <h2>Signup</h2>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId='formEmail'>
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type='email' placeholder='Enter email' value={this.state.email} onChange={this.handleFormUpdate} />
                    </Form.Group>

                    <Form.Group controlId='formPassword'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type='password' placeholder='Password' value={this.state.password} onChange={this.handleFormUpdate} />
                    </Form.Group>

                    <Button variant='primary' type='submit'>Signup</Button>
                </Form>
            </div>
        );

    }

}

const mapDispatchToProps = dispatch => ({
    userPostRegistration: userInfo => dispatch(userPostRegistration(userInfo))
});

export default connect(null, mapDispatchToProps)(Registration);
