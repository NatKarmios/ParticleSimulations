import PropTypes from 'prop-types';

//noinspection JSUnresolvedFunction,JSUnresolvedVariable
const generator_data = PropTypes.shape({
    finished: PropTypes.bool.isRequired,
    pid: PropTypes.number.isRequired,
    gist_url: PropTypes.string,
    progress: PropTypes.number.isRequired,
    type: PropTypes.string.isRequired
});

//noinspection JSUnresolvedFunction,JSUnresolvedVariable
const reply_data = PropTypes.shape({
    success: PropTypes.bool.isRequired,
    data: PropTypes.shape({
        generators: PropTypes.arrayOf(generator_data)
    })
});

export {reply_data, generator_data};

