import React from 'react';
import Cookies from 'js-cookie';
import Header from './Header';
import Body from './Body';
import swal from "sweetalert2";
import $ from "jquery";
import "sweetalert2/dist/sweetalert2.min.css"
import Fade from "./Fade";

let connection_success = false;
let running = true;
let token = null;
let reply_data = null;
let reply_pid = null;

let address = null;

const status_interval = 1000;


const misc_connection_failed_popup = () => {
    swal({
        type: 'error',
        title: 'Connection failed!',
        text: 'Something went wrong!',
        confirmButtonText: 'Uh oh!'
    }).then(()=>{}, ()=>{});
};

const add_scatter = () => {
    swal({
        title: 'Create a Scatter Data Generator',
        html: '<i>Energy step: </i><input type="number" id="scatter-input1" class="swal2-input"><br>' +
        '<i>Events per energy step: </i><input type="number" id="scatter-input2" class="swal2-input">',
        preConfirm: function () {
            return new Promise(function (resolve, reject) {
                // <editor-fold desc="Validating input">

                let energy_step_raw = $('#scatter-input1').val();
                let events_per_energy_step_raw = $('#scatter-input2').val();

                let energy_step = parseInt(energy_step_raw, 10);
                let events_per_energy_step = parseInt(events_per_energy_step_raw, 10);

                if (isNaN(energy_step) ||
                    energy_step !== parseFloat(energy_step_raw) ||
                    energy_step < 1 || energy_step > 7000) {
                    reject("'Energy step' must be an integer between 1 and 7000!");
                    return;
                }
                
                if (isNaN(events_per_energy_step) ||
                    events_per_energy_step !== parseFloat(events_per_energy_step_raw) ||
                    events_per_energy_step < 1 || events_per_energy_step > 10000) {
                    reject("'Events per energy step' must be an integer between 1 and 10,000!");
                    return;
                }

                // </editor-fold>

                console.log(token);
                $.ajax({
                    method: "POST",
                    url: "http://"+address+"/add",
                    data: JSON.stringify({
                        type: 'scatter',
                        params: {energy_step: energy_step, events_per_energy_step: events_per_energy_step}}),
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: "Basic " + btoa("admin:"+token)
                    }
                }).then(
                    (data) => {
                        connection_success = true;
                        if (data.success){
                            reply_pid = data.data.pid;
                            resolve();
                        } else {
                            reject(data.message);
                        }
                    },
                    () => {
                        connection_success = false;
                        resolve();
                    }
                );
            })
        },
        showLoaderOnConfirm: true,
        onOpen: function () {
            $('#swal-input1').focus()
        }
    }).then(() => {
        if (connection_success) {
            swal({
                type: 'success',
                title: 'Success!',
                text: 'Generator ' + reply_pid.toString() +' added!',
                confirmButtonText: 'Nice!'
            }).then(()=>{}, ()=>{});
        } else {
            misc_connection_failed_popup();
        }
    }, () => {})
};

const add_hist = () => {
    swal({
        title: 'Create a Scatter Data Generator',
        html: '<i>Energy level: </i><input type="number" id="hist-input1" class="swal2-input"><br>' +
        '<i>Number of collisions: </i><input type="number" id="hist-input2" class="swal2-input">',
        preConfirm: function () {
            return new Promise(function (resolve, reject) {
                // <editor-fold desc="Validating input">

                let energy_level_raw = $('#hist-input1').val();
                let number_of_collisions_raw = $('#hist-input2').val();

                let energy_level = parseInt(energy_level_raw, 10);
                let number_of_collisions = parseInt(number_of_collisions_raw, 10);

                if (isNaN(energy_level) ||
                    energy_level !== parseFloat(energy_level_raw) ||
                    energy_level < 7000 || energy_level > 14000) {
                    reject("'Energy level' must be an integer between 7000 and 14000!");
                    return;
                }
                
                if (isNaN(number_of_collisions) ||
                    number_of_collisions !== parseFloat(number_of_collisions_raw) ||
                    number_of_collisions < 1 || number_of_collisions > 10000) {
                    reject("'Number of collisions' must be an integer between 1 and 10,000!");
                    return;
                }

                // </editor-fold>

                console.log(token);
                $.ajax({
                    method: "POST",
                    url: "http://"+address+"/add",
                    data: JSON.stringify({
                        type: 'hist',
                        params: {energy_level: energy_level, number_of_collisions: number_of_collisions}}),
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: "Basic " + btoa("admin:"+token)
                    }
                }).then(
                    (data) => {
                        connection_success = true;
                        if (data.success){
                            reply_pid = data.data.pid;
                            resolve();
                        } else {
                            reject(data.message);
                        }
                    },
                    () => {
                        connection_success = false;
                        resolve();
                    }
                );
            })
        },
        showLoaderOnConfirm: true,
        onOpen: function () {
            $('#swal-input1').focus()
        }
    }).then(() => {
        if (connection_success) {
            swal({
                type: 'success',
                title: 'Success!',
                text: 'Generator ' + reply_pid.toString() +' added!',
                confirmButtonText: 'Nice!'
            }).then(()=>{}, ()=>{});
        } else {
            misc_connection_failed_popup();
        }
    }, () => {})
};

const delete_generator = (pid) => {
    swal({
        title: 'Delete generator ' + pid + '?',
        text: "You won't be able to revert this!",
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        showLoaderOnConfirm: true,
        preConfirm: () => {return new Promise((resolve, reject) => {
            $.ajax({
                    method: "POST",
                    url: "http://"+address+"/del",
                    data: JSON.stringify({
                        pid: pid,
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: "Basic " + btoa("admin:"+token)
                    }
                }).then(
                    (data) => {
                        connection_success = true;
                        if (data.success){
                            resolve();
                        } else {
                            reject(data.message);
                        }
                    },
                    () => {
                        connection_success = false;
                        resolve();
                    }
                );
            })
        }
    }).then(function () {
        if (connection_success) {
            swal({
                title: 'Deleted!',
                text: 'Your file has been deleted.',
                type: 'success'
            }).then(()=>{}, ()=>{});
        } else {
            misc_connection_failed_popup();
        }
    })
};

const add_generator = () => {
    swal({
        title: "Select generator type",
        text: "What kind of data do you want to generate?",
        input: "radio",
        inputOptions: {"scatter": "Scatter Diagram", "hist": "Histogram"},
        inputValidator: function (result) {
            return new Promise(function (resolve, reject) {
                if (result) {
                    resolve();
                }
                else {
                    reject("You need to select something!");
                }
            })
        }
    }).then(function (result) {
        if (result === "scatter") {
            add_scatter()
        } else if (result === "hist") {
            add_hist()
        }
    });
};


const login_popup = (preConfirm) => {
    return swal({
        title: 'Log in',
        text: 'This will let you add and remove generators.',
        input: 'password',
        inputAttributes: {
            'autocapitalize': 'off',
            'autocorrect': 'off'
        },
        confirmButtonText: 'Let\'s go!',
        showCancelButton: true,
        cancelButtonText: 'No, thanks.',
        showLoaderOnConfirm: true,
        preConfirm: preConfirm
    });
};

const cookie_popup = (cb) => {
    if (!Cookies.get('cookies-accepted')) {
        swal({
            type: 'warning',
            title: 'This site uses cookies!',
            text: "Go away if you're not alright with that.",
            confirmButtonText: "We're good!"
        }).then(() => {
            Cookies.set('cookies-accepted', true);
            cb();
        }, () => {cookie_popup(cb);});
    } else { cb() }
};

const initial_connection_failed_popup = (preConfirm) => {
    return swal({
        title: 'Failed to connect!',
        text: 'Check your connection, or ask Nat!',
        type: 'error',
        confirmButtonText: 'Try again, you fool!',
        showCancelButton: true,
        cancelButtonText: 'Try a different address',
        showLoaderOnConfirm: true,
        preConfirm: preConfirm
    });
};

const connection_success_popup = (address) => {
    swal({
        title: "Success!",
        text: "Successfully connected to '"+address+"'.",
        type: 'success'
    }).then(()=>{}, ()=>{});
};

const get_address_popup = (preConfirm) => {
    let saved_address = Cookies.get('server-address');
    return swal({
        type: 'info',
        title: 'Enter Address',
        text: "e.g. '127.0.0.1' or 'myDomain.com'",
        input: 'text',
        inputValue: saved_address ? saved_address : '',
        showLoaderOnConfirm: true,
        inputValidator: (address) => {return new Promise((resolve, reject) => {
            if (address) {
                resolve()
            } else {
                reject("Enter an address!")
            }
        })},
        preConfirm: preConfirm
    })
};


class App extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            logged_in: false,
            address: null,
            data: null
        };

        this.setInitialState = this.setInitialState.bind(this);
        this.setData = this.setData.bind(this);
        this.get_status_loop = this.get_status_loop.bind(this);
        this.checkLogin = this.checkLogin.bind(this);
        this.logIn = this.logIn.bind(this);
        this.loggedIn = this.loggedIn.bind(this)
    }

    render() {
        let logged_in = this.state.logged_in;
        return (
            <div className="App container">
                <Fade>
                    <Header add={add_generator} logged_in={logged_in} login={this.logIn} login_required={true} />
                    <Body del={delete_generator} logged_in={logged_in} data={this.state.data}/>
                </Fade>
            </div>
        );
    }

    setInitialState(data, address_) {
        Cookies.set('server-address', address_);
        this.setState({
            data: data,
            address: address_
        });
        address = address_;
        this.test_auth();
        this.get_status_loop();
    }

    setData(data) {
        this.setState({"data": data});
    }

    getInitalData(self, address) {
        return new Promise((resolve, reject) => {
            $.ajax('http://' + address + '/status').then(
                (data) => {
                    connection_success = true;
                    resolve();
                    self.setInitialState(data, address)
                },
                function (_) {
                    connection_success = false;
                    resolve();
                }
            )
        });
    }

    getAddress(self) {
        get_address_popup((address) => {
            return self.getInitalData(self, address);
        }).then(
            (address) => {
                if (!connection_success) {
                    self.connection_failed(self, address);
                } else {
                    connection_success_popup(address);
                }
            },
            () => { self.getAddress(self) }
        )
    }

    checkLogin(pass) {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: "POST",
                url: "http://"+this.state.address+"/login",
                data: JSON.stringify({pass: pass}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(
                (data) => {
                    connection_success = true;
                    if (data.success) {
                        reply_data = data;
                        this.loggedIn();
                        token = data.data.token;
                        console.log(token);
                        Cookies.set('auth-token', token);
                        resolve()
                    } else {
                        reject(data.message)
                    }
                },
                () => {
                    connection_success = false;
                    resolve()
                }
            )
        });
    }

    logIn() {
        login_popup(this.checkLogin).then(() => {
            if (connection_success) {
                swal({
                    type: 'success',
                    title: "Logged in!",
                    text: reply_data.message,
                    confirmButtonText: 'Cool!'
                }).then(() => {}, () => {})
            } else {
                misc_connection_failed_popup();
            }
        }, ()=>{});
    }

    loggedIn() {
        this.setState({logged_in: true})
    }

    connection_failed(self, address) {
        initial_connection_failed_popup(() => {
            return self.getInitalData(self, address);
        }).then(
            () => {
                if (!connection_success) {
                    self.connection_failed(self, address);
                } else {
                    connection_success_popup(address);
                }
            },
            (dismiss) => {
                if (dismiss === "cancel") {
                    self.getAddress(self)
                } else  {
                    self.connection_failed(self, address)
                }
            }
        )
    }

    get_status_loop() {
        if (!running) return;
        let self = this;
        setTimeout(() => {
            console.log("getting...");
            $.ajax("http://"+self.state.address+"/status").then(
                (data) => {
                    self.setData(data);
                    self.get_status_loop()
                },
                () => self.get_status_loop()
            )
        }, status_interval)
    }

    test_auth() {
        let token_ = Cookies.get('auth-token');
        if (token_) {
            $.ajax({
                url: "http://" + address + "/test_auth",
                headers: {
                    Authorization: "Basic " + btoa("admin:" + token_)
                }
            }).then(
                (data) => {
                    console.log("ho");
                    console.log(JSON.stringify(data));
                    if (data.success) {
                        this.loggedIn();
                        token = token_;
                    } else {}
                }, () => {}
            );
        }
    }

    componentWillMount() {
        cookie_popup((cb) => {
            this.getAddress(this);
        });
    }
}
export default App;

