import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import Login from "./Components/Login/Login";
import { ChakraProvider } from "@chakra-ui/react";
import reportWebVitals from "./reportWebVitals";
import { initFacebookSdk } from "./Helpers/facebookHelpers";

// wait for facebook sdk before startup
initFacebookSdk().then(startApp);

function startApp() {
  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(
    <React.StrictMode>
      <ChakraProvider>
        <Login>
          <App />
        </Login>
      </ChakraProvider>
    </React.StrictMode>
  );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
