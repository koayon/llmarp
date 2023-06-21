import React, { Component, useEffect, useRef, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

interface AppState {
  currentIndex: number;
  score: number;
  lmScore: number; // score for the language model
  currentGuess: string;
  model: any;
}

interface AppProps {}

// class App extends Component<AppProps, AppState> {
//   sentence: string;
//   words: string[];

//   constructor(props: AppProps) {
//     super(props);

//     this.sentence = "React is a popular library for building user interfaces";
//     this.words = this.sentence.split(" ");

//     this.state = {
//       currentIndex: 0,
//       score: 0,
//       lmScore: 0,
//       currentGuess: "",
//       model: null,
//     };

//     this.handleSubmit = this.handleSubmit.bind(this);
//     this.handleInputChange = this.handleInputChange.bind(this);
//   }

//   async componentDidMount() {
//     const model = await this.DefineModel();
//     this.setState({ model });
//   }

//   handleInputChange = (event) => {
//     this.setState({
//       currentGuess: event.target.value,
//     });
//   };

//   handleSubmit = async (event) => {
//     event.preventDefault();

//     if (this.state.model) {
//       const inputTokens = await this.state.model.tokenizer.encode(
//         this.words.slice(0, this.state.currentIndex).join(" ")
//       );
//       const predictedToken = await this.predictNextToken(
//         inputTokens,
//         this.state.model
//       );
//       const predictedWord = this.state.model.tokenizer.decode([predictedToken]);

//       let newLmScore = this.state.lmScore;
//       if (predictedWord === this.words[this.state.currentIndex]) {
//         newLmScore++;
//       }

//       let newUserScore = this.state.score;
//       if (this.state.currentGuess === this.words[this.state.currentIndex]) {
//         newUserScore++;
//       }

//       this.setState((prevState) => ({
//         score: newUserScore,
//         currentIndex: prevState.currentIndex + 1,
//         currentGuess: "",
//         lmScore: newLmScore,
//       }));
//     }
//   };

//   async DefineModel() {
//     const model = await pipeline("text-generation");
//     return model;
//   }

//   async predictNextToken(inputTokens: number[], model: any) {
//     const nextToken = await model.generate(inputTokens, {
//       max_new_tokens: 1,
//     });
//     return nextToken;
//   }

//   render() {
//     const isGuessDisabled = !this.state.currentGuess;
//     return (
//       <div>
//         <h1>Guess the Next Word</h1>
//         <p>
//           Your Score: {this.state.score} / {this.state.currentIndex}
//           <br></br>
//           Transformer Score: {this.state.lmScore} / {this.state.currentIndex}
//         </p>
//         {
//           <p>
//             Sentence: {this.words.slice(0, this.state.currentIndex).join(" ")}
//           </p>
//         }
//         <form onSubmit={this.handleSubmit}>
//           <input
//             type="text"
//             onChange={this.handleInputChange}
//             value={this.state.currentGuess}
//           />
//           <input type="submit" value="Guess" disabled={isGuessDisabled} />
//         </form>
//       </div>
//     );
//   }
// }

async function helloWorld() {
  // Allocate a pipeline for sentiment-analysis
  let pipe = await pipeline("sentiment-analysis");
  let out = await pipe("I love transformers!");
  // [{'label': 'POSITIVE', 'score': 0.999817686}]
  return out;
}

class App extends Component {
  async componentDidMount() {
    console.log("Hello World");
    const result = await helloWorld();
    console.log(result);
  }

  render() {
    return <div>App Component</div>;
  }
}

export default App;
