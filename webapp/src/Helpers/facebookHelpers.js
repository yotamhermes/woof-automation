const facebookAppId = 172873165789869; // process.env.REACT_APP_FACEBOOK_APP_ID;

export function initFacebookSdk() {
  return new Promise((resolve) => {
    window.fbAsyncInit = function () {
      window.FB.init({
        appId: facebookAppId,
        cookie: true,
        xfbml: true,
        version: "v8.0",
      });

      resolve();
    };

    window.onunload = () => {
      fbLogout();
    };

    // load facebook sdk script
    (function (d, s, id) {
      var js,
        fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {
        return;
      }
      js = d.createElement(s);
      js.id = id;
      js.src = "https://connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    })(document, "script", "facebook-jssdk");
  });
}

export function fbLogin(onLogin) {
  window.FB.login(onLogin, {
    auth_type: "rerequest",
    scope: "public_profile,email,instagram_content_publish",
  });
}

export function fbLogout(onLogout) {
  window.FB.logout(onLogout, {
    access_token: document.cookie,
  });
}
