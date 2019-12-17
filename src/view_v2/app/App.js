import React from 'react';
import { Nav, Navbar, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

import Routes from './Routes';

export default function App(props) {

    return (
        <div className='App container'>
            <Navbar bg='light' expand='lg' className='header_bar'>
                <Navbar.Brand href='/'>Home</Navbar.Brand>
                <Navbar.Toggle aria-controls='basic-navbar-nav' />
                <Navbar.Collapse>
                    <Nav className='navbar'>
                        <LinkContainer to='/register' className='link'>
                            <NavItem>Signup</NavItem>
                        </LinkContainer>
                        <LinkContainer to='/login' className='link'>
                            <NavItem>Login</NavItem>
                        </LinkContainer>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
            <Routes />
        </div>
    );

}
