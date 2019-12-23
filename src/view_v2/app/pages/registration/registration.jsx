import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, Form } from 'react-bootstrap';
import PropTypes from 'prop-types';

import { userPostRegistration } from '../../modules/actions';

import './registration.less';
class Registration extends Component {

    constructor(props) {

        super(props);
        this.state = {
            username: '',
            password: ''
        };

    }

    handleFormUpdate = event => {

        this.setState({
            [event.target.name]: event.target.value
        });

    }

    handleSubmit = event => {

        event.preventDefault();
        this.props.userPostRegistration(this.state);

    }

    render() {

        return (
            <div className='container'>
                <h2>Signup</h2>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId='formEmail'>
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type='email' placeholder='Enter email' values={this.state.username}
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

Registration.propTypes = {
    username: PropTypes.string,
    userPostRegistration: PropTypes.func
};

const mapDispatchToProps = dispatch => ({
    userPostRegistration: userInfo => dispatch(userPostRegistration(userInfo))
});

export default connect(null, mapDispatchToProps)(Registration);
