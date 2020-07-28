import React from 'react';
import '../App.css';
import { Switch, Route, Link, useRouteMatch } from 'react-router-dom';

function Host() {
    let match = useRouteMatch();

    return (
        <div>
            <p>This is host number {match.params.ip}</p>
        </div>
    )
}

export default Host;