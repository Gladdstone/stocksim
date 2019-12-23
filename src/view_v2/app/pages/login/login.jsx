import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, Form } from 'react-bootstrap';
import PropTypes from 'prop-types';

import { userPostLogin } from '../../modules/actions';

import './login.less';

class Login extends Component {

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

        this.props.userPostLogin(this.state);

    }

    render() {

        return (
            <div className='container'>
                <h2>Login</h2>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId='formEmail'>
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type='email' placeholder='Enter email' values={this.state.email}
                            onChange={this.handleFormUpdate} />
                    </Form.Group>

                    <Form.Group controlId='formPassword'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control type='password' placeholder='Password' values={this.state.password}
                            onChange={this.handleFormUpdate} />
                    </Form.Group>

                    <Button variant='primary' type='submit'>Submit</Button>
                </Form>
            </div>
        );

    }

}

Login.propTypes = {
    email: PropTypes.string,
    userPostLogin: PropTypes.func
};

const mapDispatchToProps = dispatch => ({
    userPostLogin: userInfo => dispatch(userPostLogin(userInfo))
});

export default connect(null, mapDispatchToProps)(Login);
