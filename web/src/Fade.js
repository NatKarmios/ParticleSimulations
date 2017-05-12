import React from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';

const Fade = (props) => {
    return (
        <ReactCSSTransitionGroup
            transitionName="myFade"
            transitionEnterTimeout={700}
            transitionLeaveTimeout={700}
            transitionAppear={true}
            transitionAppearTimeout={500}
        >
            {props.children}
        </ReactCSSTransitionGroup>
    );
};

export default Fade;