import React, { Component } from 'react';
import { render } from "react-dom";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loader: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("api/cookbook/recipes/feed")
            .then(response => {
                if (response.status > 400) {
                    return this.setState(() => {
                        return { placeholder: "Something went wrong!" };
                    });
                }
                return response.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true,
                    };
                });
            });
    }

    render() {
        return (
            <ul>
                {this.state.data.map(recipe => {
                    return (
                        <li key={recipe.url}>
                            {recipe.title}
                        </li>
                    );
                })}
            </ul>
        )
    }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);