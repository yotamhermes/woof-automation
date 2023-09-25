import axios from "axios";

const API_KEY = "aUIAPxb3pba5co7AXUp0V3S3C7ShrIjJ83W06VUh"; //process.env.REACT_APP_WOOF_API_KEY;
const URL = "https://lomye7y9bc.execute-api.us-east-1.amazonaws.com/prod/"; // process.env.REACT_APP_WOOF_URL;

const service = axios.create({
  baseURL: URL,
  headers: { "x-api-key": API_KEY },
});

export function getPostsSuggestions() {
  const postSuggestions = service.get(`/get-posts-suggestions`);
  return postSuggestions;
}

export function markPostsAsDone(prompt_id) {}
