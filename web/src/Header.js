import React from 'react';
import PropTypes from 'prop-types';
import "./Header.css"
import {Button, Nav, Navbar, NavItem} from 'react-bootstrap'

class Header extends React.Component {
    render (){
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#"><h2>Particle Data Generation</h2></a>
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav className="pull-right">
                    <NavItem>
                        <Button disabled={this.props.logged_in} onClick={this.props.login} >
                            <i className={"fa " + (this.props.logged_in ? "fa-unlock" : "fa-lock")} />
                            {this.props.login_required ?
                                (this.props.logged_in ? " Logged in" : " Log in") :
                                " No login required."}
                        </Button>
                        <Button disabled={!this.props.logged_in} bsStyle="primary" onClick={this.props.add}>
                            <i className="fa fa-plus-circle"/> Add a generator
                        </Button>
                    </NavItem>
                </Nav>
            </Navbar>
        );
    }
}

//noinspection JSUnresolvedVariable
Header.propTypes = {
    logged_in: PropTypes.bool.isRequired,
    login_required: PropTypes.bool.isRequired,
    add: PropTypes.func.isRequired,
    login: PropTypes.func.isRequired
};

export default Header;
