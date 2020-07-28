import React from 'react';
import '../App.css';
import '../css/style.css'
import { Switch, Route, Link } from 'react-router-dom';
import Host from './Host';

import 'react-bulma-components/dist/react-bulma-components.min.css';
import { Button, Container, Columns, Level, Box } from 'react-bulma-components';


class PortInfo extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            port: props.port
        }
    }

    render() {
        return (
        <Columns.Column size={2}>
            <Button color="info">{this.state.port}</Button>
        </Columns.Column>
        )
    }
}

class HostInfo extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            host: props.host,
            stat_waiting: false
        }
    }

    ping = () => {
        this.setState({
            ...this.state,
            stat_waiting: true
        });

        const ip = this.state.host.ip;
        fetch("/isup/{ip}").then(res => res.json())
            .then(result => {
                let status = result['up'];
                console.log(status);

                this.setState({
                    ...this.state,
                    host: {
                        ...this.state.host,
                        isup: status,
                    },
                    stat_waiting: false
                });

                console.log('new state ' + this.state.host.isup);
            });
    }

    render() {
        console.log('render state ' + this.state.host.isup);
        let stat_symb = this.state.stat_waiting ? "waiting..." :
            (this.state.host.isup ? "ONLINE" : "OFFLINE");

        const ports = this.state.host.ports.map( p => <PortInfo key={`${this.state.host.ip}:${p}`} port={p} /> )

        return (
            <div className="hostInfo">

                <Columns gapless>
                        <Columns.Column size={2}>
                            <Link to={`/host/${this.state.host.ip}`}>444.444.444.444</Link>
                        </Columns.Column>

                        <Columns.Column size={2}>
                            <p>{stat_symb}</p>
                        </Columns.Column>

                        <Columns.Column size={1}>
                        
                            <Button color="info" onClick={this.ping} outlined size="small">
                                    Ping
                            </Button>

                        </Columns.Column>
                </Columns>

                <Columns gapless>
                    {ports}
                </Columns>

                
            </div>
        )
    }
}


function updateHostList(h) {
    this.setState({ hosts: h })
}

class HostList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            hosts: [],
        }
    }

    componentDidMount() {
        updateHostList = updateHostList.bind(this);
    }

    pingAllClick = (e) => {
        e.preventDefault();

        this.state.hosts.forEach(h => {
            this.ping(h['ip']);
        });

        console.log(this.state.status);
    }

    render() {
        const hosts_list = this.state.hosts.map(h => <HostInfo key={h.ip} host={h} />)

        return (
            <div>
                <button onClick={this.pingAllClick}>Ping All</button>
                <p>List of hosts:</p>

                <Columns>
                    <Columns.Column size={8} offset={2}>
                        <ul>
                            {hosts_list}
                        </ul>
                    </Columns.Column>
                </Columns>
            </div>
        )
    }

}

class Landing extends React.Component {

    componentDidMount() {
        fetch("/hosts").then(res => res.json())
            .then(result => {
                console.log(result);
                updateHostList(result['hosts']);
            });
    }

    render() {
        return (
            <div>
                <Container>
                    <button onClick={this.refreshButtonClick}>Refresh</button>
                    <HostList />
                </Container>
            </div>
        )
    }
}

export default Landing;