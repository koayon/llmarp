import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

class App extends Component {
  constructor(props) {
    super(props);

    this.sentence = "React is a popular library for building user interfaces";
    this.words = this.sentence.split(" ");

    this.state = {
      currentIndex: 0,
      score: 0,
      currentGuess: "",
    };
  }

  handleInputChange = (event) => {
    this.setState({
      currentGuess: event.target.value,
    });
  };

  handleSubmit = (event) => {
    event.preventDefault();

    if (this.state.currentGuess === this.words[this.state.currentIndex]) {
      this.setState((state) => ({
        score: state.score + 1,
        currentIndex: state.currentIndex + 1,
        currentGuess: "",
      }));
    } else {
      this.setState((state) => ({
        currentIndex: state.currentIndex + 1,
        currentGuess: "",
      }));
    }
  };

  render() {
    return (
      <div>
        <h1>Guess the Next Word</h1>
        <p>
          Your Score: {this.state.score} / {this.state.currentIndex}
          <br></br>
          Transformer Score: {this.state.currentIndex} /{" "}
          {this.state.currentIndex}
        </p>
        {
          <p>
            Sentence: {this.words.slice(0, this.state.currentIndex).join(" ")}
          </p>
        }
        <form onSubmit={this.handleSubmit}>
          <input
            type="text"
            onChange={this.handleInputChange}
            value={this.state.currentGuess}
          />
          <input type="submit" value="Guess" />
        </form>
      </div>
    );
  }
}

export default App;
