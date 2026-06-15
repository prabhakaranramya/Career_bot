import { useState } from "react";
import ChatWindow from "./ChatWindow";
import "./App.css";

export default function App() {
  const [started, setStarted] = useState(false);

  return (
    <div className="app">
      {!started ? (
        <div className="landing">
          <div className="landing-card">
            <img src="/avatar.png" alt="CareerCompass AI" className="avatar-image" />
           <h1>Meet <span className="accent">CareerCompass AI</span></h1>
           <p className="tagline">Your personal AI career guide.<br />Let's build your future, one step at a time.</p>
            <button className="start-btn" onClick={() => setStarted(true)}>
              Start Career Chat →
            </button>
          </div>
        </div>
      ) : (
        <ChatWindow />
      )}
    </div>
  );
}