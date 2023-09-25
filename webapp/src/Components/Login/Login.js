import { useState } from "react";
import LoginButton from "./LoginButton";
import { fbLogin } from "../../Helpers/facebookHelpers";

function Login({ children }) {
  const [login, updateLoginState] = useState(false);

  const fbLoginCallback = (response) => {
    if (response.status === "connected") {
      updateLoginState(true);
      document.cookie = `${response.access_token}`;
    } else {
      // The person is not logged into your webpage or we are unable to tell.
    }
  };

  return login ? (
    <div>{children}</div>
  ) : (
    <LoginButton onClick={() => fbLogin(fbLoginCallback)} />
  );
}

export default Login;
