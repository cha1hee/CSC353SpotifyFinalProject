var redirect = "http://localhost:3000/logged";

var client_id = "";
var client_secret = "";

const AUTHORIZE = "https://accounts.spotify.com/authorize";

const TOKEN = "https://accounts.spotify.com/api/token";

function authorize() {
  let url = AUTHORIZE;
  url += "?client_id" + clident_id;
  url += "&response_type=code";
  url += "&redirect_uri" + encodeURI(redirect);
  url += "&show_dialog=true";
  url +=
    "&scope=user-read-private user-read-email user-read-playback-state user-top-read";
  window.location.href = url;
}

function onPageLoad() {
  if (window.location.search.length > 0) {
    handleRedirect();
  } else {
    getSong();
  }
}
