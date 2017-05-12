import React from 'react'
import PropTypes from 'prop-types';

import "./Body.css"
import {ListGroup} from 'react-bootstrap'
import Listing from "./Listing";
import {reply_data} from "./object_shapes";
import Loading from './Loading';

class Body extends React.Component {

    render() {
        if (!this.props.data) {
            return (<Loading />);
        }

        let listings = [];
        this.props.data.data.generators.forEach((listing_data) => {listings.push(
            <Listing del={this.props.del} logged_in={this.props.logged_in} data={listing_data}/>
        )});

        if (listings.length===0) {
            return (
                <div className="text-center" style={{width: "auto"}}>
                    <h2>There are no generators!</h2>
                </div>
            );
        }
        
        return (
            <ListGroup>
                {listings}
            </ListGroup>
        );
    }
}

//noinspection JSUnresolvedVariable
Body.propTypes = {
    del: PropTypes.func.isRequired,
    logged_in: PropTypes.bool.isRequired,
    data: reply_data
};

export default Body;
