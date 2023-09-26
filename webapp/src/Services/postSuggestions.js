import axios from "axios";

const API_KEY = process.env.REACT_APP_WOOF_API_KEY;
const URL = process.env.REACT_APP_WOOF_URL;

const service = axios.create({
  baseURL: URL,
  headers: {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
  },
});

export function getPostsSuggestions() {
  const postSuggestions = service.get(`/get-posts-suggestions`);
  return postSuggestions;
}

export function markPostsAsDone(prompt_id) {}
