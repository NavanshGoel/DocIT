import React, { useState } from "react";
import { BrowserRouter, Route, Link, Redirect } from "react-router-dom";
import SpeechRecognition, {
  useSpeechRecognition
} from "react-speech-recognition";
import "./App.css"
import logo from "./logo.png"

function App() {

  const commands = [
    {
      command: ["Go to * page", "Go to *", "Open * page", "Open *"],
      callback: (redirectPage) => setRedirectUrl(redirectPage)
    }
  ];

  const { transcript } = useSpeechRecognition({ commands });
  const [redirectUrl, setRedirectUrl] = useState("");
  const pages = ["dashboard", "appointment", "news", "calendar", "nutrition", "settings"];
  const urls = {
    dashboard: "/dashboard",
    appointment: "/appointment",
    news: "/news",
    calendar: "/calendar",
    nutrition: "/nutriton",
    settings: "/settings"
  };

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return null;
  }

  let redirect = "";

  if (redirectUrl) {
    if (pages.includes(redirectUrl)) {
      redirect = <Redirect to={urls[redirectUrl]} />;
    } else {
      redirect = <p>Could not find page: {redirectUrl}</p>;
    }
  }

  return (
    <div className="App">
      <img src={logo} class="logo"></img>
      <BrowserRouter>
        <div class="p1">
          <h1 class='heading'>Voice Control Panel</h1>
          <p>You can say:</p>
          <p>* Go to dashboard</p>
          <p>* Go to appointment</p>
          <p>* Go to calendar</p>
          <p>* Go to news</p>
          <p>* Go to nutrition</p>
          <p>* Go to settings</p>
        </div>

        <Route
          path="/dashboard"
          render={() => (window.location = "https://doc-itapp.herokuapp.com/dashboardp")}
        />
        <Route
          path="/appointment"
          render={() => (window.location = "https://doc-itapp.herokuapp.com/appointments.html")}
        />
        <Route
          path="/news"
          render={() =>
            (window.location = "https://doc-itapp.herokuapp.com/newsp.html")
          }
        />
        <Route
          path="/calendar"
          render={() => (window.location = "https://doc-itapp.herokuapp.com/calendarp.html")}
        />

        <Route
          path="/nutrition"
          render={() => (window.location = "https://doc-itapp.herokuapp.com/nutrition.html")}
        />

        <Route
          path="/settings"
          render={() => (window.location = "https://doc-itapp.herokuapp.com/settings.html")}
        />
        {redirect}
      </BrowserRouter>
     
      <div class="p2">
        <p id="transcript" style={{marginLeft:'40%'}}>Live Captions:</p>
        <p>{transcript}</p>
      <br />
      <button onClick={SpeechRecognition.startListening} className="button">Voice</button>
      </div>
    </div>
  );
}

export default App;
