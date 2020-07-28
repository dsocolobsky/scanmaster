import React from 'react';
import '../App.css';
import { Switch, Route, Link } from 'react-router-dom';
import Host from './Host';

function Landing() {
    return (
        <div>
            <p>Landing page</p>
            <Link to='/host/123'>Host 123</Link>
            <br></br>
            <Link to='/host/222'>Host 222</Link>
        </div>
    )
}

export default Landing;