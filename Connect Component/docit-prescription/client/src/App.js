import TextEditor from "./TextEditor"
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom"
import { v4 as uuidV4 } from "uuid"
import logo from "./logo.png";
import "./App.css"


const currentURL = window.location.href;

function App() {


  return (
    <div>
    <Router>
      <Switch>
        <Route path="/" exact>
          <Redirect to={`/documents/${uuidV4()}`} />
        </Route>
        <Route path="/documents/:id">
          <p style={{display: "none"}}>
            {currentURL}
          </p>
          <div className="logo">
            <img src={logo} width="200px" height="100px"></img>
          </div>
          <TextEditor />
        </Route>
      </Switch>
    </Router>
    </div>
  )
}

export default App
