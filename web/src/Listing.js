import React from 'react';
import PropTypes from 'prop-types';
import {Button, ButtonGroup, Col, ListGroupItem, ProgressBar, Row, Label} from "react-bootstrap";
import {generator_data} from "./object_shapes";

const generator_types = {
    scatter: "Scatter",
    hist: "Histogram"
};

class Listing extends React.Component {

    render() {
        let del = this.props.del;
        let logged_in = this.props.logged_in;
        let data = this.props.data;
        let progress = Math.floor(data.progress * 100);
        let finished = data.finished;
        return (
            <ListGroupItem>
                <Row>
                    <Col lg={2} className="text-center">
                        <Label>{generator_types[data.type]}</Label> Generator {data.pid}
                    </Col>
                    <Col lg={8}>
                        <ProgressBar
                            striped
                            active={!finished}
                            now={progress}
                            bsStyle={finished ? "success" : null}
                        />
                    </Col>
                    <Col lg={2} className="text-center">
                        <ButtonGroup bsSize="xsmall">
                            <Button
                                disabled={!finished}
                                bsStyle={finished ? "primary" : "default"}
                                onClick={finished ? function () {
                                    window.open(data.gist_url)
                                } : null}
                            >
                                <i className="fa fa-table"/> <i>Data</i>
                            </Button>
                            <Button
                                disabled={!logged_in}
                                bsStyle="danger"
                                onClick={function () {
                                    del(data.pid)
                                }}
                            >
                                <i className="fa fa-trash-o"/> <i>Delete</i>
                            </Button>
                        </ButtonGroup>
                    </Col>
                </Row>
            </ListGroupItem>
        );
    }
}

//noinspection JSUnresolvedVariable
Listing.propTypes = {
    del: PropTypes.func.isRequired,
    logged_in: PropTypes.bool.isRequired,
    data: generator_data.isRequired
};

export default Listing;
