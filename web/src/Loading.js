import React from 'react';
import Fade from "./Fade";

const Loading = () => (
    <Fade>
        <div key={true} className="text-center" style={{width: "auto"}}>
            <h3>
                Connecting...
                <br /><br />
                <i className="fa fa-cog fa-spin fa-3x fa-fw" />
            </h3>
        </div>
    </Fade>
);

export default Loading;