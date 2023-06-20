import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { pipeline } from "@xenova/transformers";

class App extends Component {
  sentence: string;
  words: string[];

  state = {
    currentIndex: 0,
    score: 0,
    currentGuess: "",
  };

  model = DefineModel();

  constructor(props) {
    super(props);

    this.sentence = "React is a popular library for building user interfaces";
    this.words = this.sentence.split(" ");

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange = (event) => {
    this.setState({
      currentGuess: event.target.value,
    });
  };

  handleSubmit = (event) => {
    event.preventDefault();

    if (this.state.currentGuess === this.words[this.state.currentIndex]) {
      this.setState(() => ({
        score: this.state.score + 1,
        currentIndex: this.state.currentIndex + 1,
        currentGuess: "",
      }));
    } else {
      this.setState(() => ({
        currentIndex: this.state.currentIndex + 1,
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

async function DefineModel() {
  const model = await pipeline("text-generation");
  return model;
}

async function TokenizeSentence(input_sentence: string, model: any) {
  return await model.tokenizer.encode(input_sentence);
}

async function GenerateSentence(tokens: Array<number>, model: any) {
  // const sentence = "Hello my name is Kola".split(" ");

  const predictions: Array<number> = [];
  const firstTokens: Array<Array<number>> = [];
  for (let i = 0; i < tokens.length; i++) {
    firstTokens.push(tokens.slice(0, i + 1));
  }

  for (let i = 0; i < firstTokens.length; i++) {
    const output = await predictNextToken(firstTokens[i], model);
    predictions.push(output);
  }
  return predictions;
}

async function predictNextToken(inputTokens: number[], model: any) {
  // Load the model and the tokenizer

  // Tokenize the input sentence and get the input IDs
  // const inputs = await model.tokenizer.encode(sentence);

  // Generate the next token
  const nextToken = await model.model.generate(inputTokens, {
    max_new_tokens: 1,
  });

  // Decode the output token back into text
  // const nextToken = await model.tokenizer.decode(outputs[0], {
  //   skip_special_tokens: true,
  // });

  return nextToken;
}

export default App;
